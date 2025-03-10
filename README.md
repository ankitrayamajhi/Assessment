---

# **GreenTick Security Tools**
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

Security monitoring solutions for log analysis and web vulnerability scanning.

---

## **Table of Contents**
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Assumptions](#assumptions)
- [Limitations](#limitations)
- [Sample Output](#sample-output)
- [Testing](#testing)

---

## **Project Overview**

This repository contains two security tools developed as part of GreenTick's internship assessment:

1. **SystemMonitor**  
   - Monitors log files for security-related events.  
   - Generates real-time alerts for unauthorized access, failed logins, and suspicious activity.

2. **WebScanCrawler**  
   - Crawls websites to identify vulnerabilities.  
   - Detects missing security headers, outdated software versions, and insecure forms.

---

## **Features**

### **SystemMonitor**
✅ Detects:  
   - Failed login attempts  
   - Unauthorized access  
   - Suspicious security events  
✅ Additional:  
   - Extracts timestamps in `YYYY-MM-DD HH:MM:SS` format  
   - Case-insensitive pattern matching  
   - Handles improperly formatted log entries gracefully  

### **WebScanCrawler**
✅ Detects:  
   - Missing HTTP security headers (`Strict-Transport-Security`, `X-Content-Type-Options`)  
   - Outdated software versions (Apache, WordPress, nginx)  
   - Insecure forms (use of `GET` method, missing `action` attributes)  
✅ Additional:  
   - Recursive crawling with configurable depth  
   - Identifies software version disclosures from server headers  

---

## **Project Structure**

```
Assessment/
├── system_monitor.py   # Log analysis tool
├── web_crawler.py      # Web vulnerability scanner
├── test.log            # Sample log file for testing
├── requirements.txt    # Dependencies (requests, bs4, etc.)
├── README.md           # Documentation
└── myenv/              # Virtual environment (gitignored)
```

> **Note:** `myenv/` is ignored in Git; users should create their own virtual environment.

---

## **Setup & Installation**

### **1. Clone Repository**
```bash
git clone https://github.com/ankitrayamajhi/Assessment.git
cd Assessment
```

### **2. Set Up Virtual Environment**
```bash
python -m venv myenv          # Create virtual environment
source myenv/bin/activate     # macOS/Linux
myenv\Scripts\activate        # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Prepare Test Log Data**  
Create a file named `test.log` with sample security events:
```
2024-12-22 10:45:00 WARNING: Unauthorized access attempt
2024-12-22 10:46:00 ERROR: Failed login for user 'admin'
```

---

## **Usage**

### **SystemMonitor**
Run the log monitoring tool:
```bash
python system_monitor.py test.log
```
**Expected Output:**
```
ALERT: UNAUTHORIZED ACCESS DETECTED AT 2024-12-22 10:45:00
ALERT: FAILED LOGIN DETECTED AT 2024-12-22 10:46:00
```

---

### **WebScanCrawler**
Run the web crawler on a target website:
```bash
python web_crawler.py http://example.com
```
**Expected Output:**
```
VULNERABILITY REPORT FOR http://example.com:
- MISSING HEADERS: Strict-Transport-Security, X-Content-Type-Options
- OUTDATED SOFTWARE: Apache 2.4.6
```

---

## **Assumptions**

### **SystemMonitor**
- Log entries follow the `YYYY-MM-DD HH:MM:SS` timestamp format.
- Each log line contains at most one security-related event.
- Pattern matching is case-insensitive.

### **WebScanCrawler**
- Crawling depth defaults to **2** unless specified.
- Websites disclose server headers with version information.
- Forms use either `GET` or `POST` methods.

---

## **Limitations**

### **SystemMonitor**
⚠️ **Limitations**:  
- Does not analyze live system logs (requires a static log file).  
- Regex-based pattern matching may result in false positives.  
- Does not analyze contextual relationships between events.  

### **WebScanCrawler**
⚠️ **Limitations**:  
- Can only detect publicly exposed security misconfigurations.  
- May fail if headers are intentionally obfuscated by the server.  
- No active exploitation or penetration testing—only passive analysis.  

---

## **Sample Output Screenshots**

### **SystemMonitor**
```
ALERT: UNAUTHORIZED ACCESS DETECTED AT 2024-12-22 10:45:00
ALERT: FAILED LOGIN DETECTED AT 2024-12-22 10:46:00
```

### **WebScanCrawler**
```
VULNERABILITY REPORT FOR http://example.com:
- MISSING HEADERS: Strict-Transport-Security, X-Content-Type-Options
- OUTDATED SOFTWARE: Apache 2.4.6
```

---

## **Testing**

### **SystemMonitor**
Test with an invalid log format:
```bash
echo "Invalid log entry without timestamp" > invalid.log
python system_monitor.py invalid.log  # Should handle gracefully
```

### **WebScanCrawler**
Test using a local HTTP server:
```bash
python -m http.server 8000 &
python web_crawler.py http://localhost:8000
```
> **Note:** The local server test won't simulate real vulnerabilities but helps check functionality.

---
