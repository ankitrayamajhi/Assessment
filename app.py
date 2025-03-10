from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# SystemMonitor Endpoint
@app.route('/monitor', methods=['POST'])
def monitor():
    log_file = request.files.get('log_file')
    if not log_file:
        return jsonify(error="No log file provided"), 400
    
    log_file.save('temp.log')
    result = subprocess.run(
        ['python', 'system_monitor.py', 'temp.log'],
        capture_output=True,
        text=True
    )
    return jsonify(output=result.stdout)

# WebScanCrawler Endpoint
@app.route('/scan', methods=['POST'])
def scan():
    url = request.json.get('url')
    if not url:
        return jsonify(error="No URL provided"), 400
    
    result = subprocess.run(
        ['python', 'web_crawler.py', url],
        capture_output=True,
        text=True
    )
    return jsonify(output=result.stdout)

if __name__ == '__main__':
    app.run(debug=False)