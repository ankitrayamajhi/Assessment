import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from packaging import version
import re

class WebCrawler:
    def __init__(self, start_url, max_depth=2):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited = set()
        self.max_depth = max_depth
        self.report = []
        self.outdated_versions = {
            'Apache': '2.4.6',
            'WordPress': '5.0',
            'nginx': '1.14.0'
        }
        self.software_pattern = re.compile(r'([A-Za-z]+)[\/ ]([\d.]+)')

    def crawl(self, url=None, current_depth=0):
        """Recursively crawl pages and collect vulnerabilities"""
        if not url:
            url = self.start_url
            
        if current_depth > self.max_depth or url in self.visited:
            return
        self.visited.add(url)
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.report.append(f"Error fetching {url}: {str(e)}")
            return

        self.check_headers(response.headers)
        self.check_software_versions(response.headers)
        self.check_forms(response.text, url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        self.check_html_versions(soup)
        
        for link in self.extract_links(soup, url):
            self.crawl(link, current_depth + 1)

    def check_headers(self, headers):
        """Check for missing security headers"""
        required = {'Strict-Transport-Security', 'X-Content-Type-Options'}
        missing = required - headers.keys()
        if missing:
            self.report.append(f"MISSING HEADERS: {', '.join(missing)} on {self.start_url}")

    def check_software_versions(self, headers):
        """Check server headers for outdated software"""
        for header in ['Server', 'X-Powered-By']:
            if header not in headers:
                continue
                
            matches = self.software_pattern.findall(headers[header])
            for software, ver in matches:
                if software in self.outdated_versions:
                    current_ver = version.parse(ver)
                    outdated_ver = version.parse(self.outdated_versions[software])
                    if current_ver <= outdated_ver:
                        self.report.append(f"OUTDATED SOFTWARE: {software} {ver} on {self.start_url}")

    def check_html_versions(self, soup):
        """Check HTML content for software version disclosures"""
        text = soup.get_text()
        for software, pattern in {
            'WordPress': r'WordPress (\d+\.\d+\.\d+)',
            'Drupal': r'Drupal (\d+\.\d+)',
            'Joomla': r'Joomla! (\d+\.\d+\.\d+)'
        }.items():
            matches = re.findall(pattern, text)
            for ver in matches:
                self.report.append(f"SOFTWARE DISCLOSURE: {software} {ver} on {self.start_url}")

    def check_forms(self, html, url):
        """Check forms for security issues"""
        soup = BeautifulSoup(html, 'html.parser')
        for form in soup.find_all('form'):
            method = form.get('method', 'GET').upper()
            action = form.get('action', '')
            
            issues = []
            if method == 'GET':
                issues.append("Uses GET method")
            if not action:
                issues.append("Missing action attribute")
                
            if issues:
                self.report.append(
                    f"INSECURE FORM on {url}: {'; '.join(issues)} (Action: {action})"
                )

    def extract_links(self, soup, base_url):
        """Extract valid same-domain links"""
        links = set()
        for a in soup.find_all('a', href=True):
            full_url = urljoin(base_url, a['href'])
            parsed = urlparse(full_url)
            if parsed.netloc == self.domain and parsed.scheme in ['http', 'https']:
                links.add(full_url)
        return links

    def generate_report(self):
        """Print formatted vulnerability report"""
        print(f"\nVULNERABILITY REPORT FOR {self.start_url}:")
        for entry in self.report:
            print(f"- {entry}")

if __name__ == "__main__":
    crawler = WebCrawler(start_url='http://example.com', max_depth=2)
    crawler.crawl()
    crawler.generate_report()