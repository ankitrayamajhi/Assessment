import re
import sys

def monitor_logs(file_path):
    """Detects security patterns in logs and generates alerts with timestamps."""
    
    PATTERNS = {
        'failed login': 'FAILED LOGIN',
        'unauthorized access': 'UNAUTHORIZED ACCESS',
        'malicious activity detected': 'MALICIOUS ACTIVITY'
    }
    TIMESTAMP_REGEX = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_lower = line.lower().strip()
                
                # Check for security patterns
                for pattern, alert in PATTERNS.items():
                    if pattern in line_lower:
                        timestamp = TIMESTAMP_REGEX.match(line)
                        time_str = timestamp.group(1) if timestamp else "NO TIMESTAMP"
                        print(f"ALERT: {alert} DETECTED AT {time_str}")
                        break  # Stop after first match per line

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python system_monitor.py <LOG_FILE_PATH>")
        sys.exit(1)
    monitor_logs(sys.argv[1])