File Integrity Monitoring (FIM) Tool

Overview

This project is a Python-based File Integrity Monitoring (FIM) tool designed to detect unauthorized changes to critical system files. It uses SHA256 hashing to establish a trusted baseline and continuously checks for modifications, deletions, or newly created files.

The tool also provides alerting via email and generates structured JSON output suitable for integration with SIEM systems.

---

Features

- Baseline creation for trusted system state
- Detection of modified, missing, and newly created files
- Multi-threaded file scanning for improved performance
- SMTP email alerting for detected changes
- JSON alert output for SIEM ingestion
- Configurable monitoring paths and settings
- Logging of all activities

---

How It Works

1. A baseline is created by hashing selected files on a clean system
2. During checks, current file states are compared against the baseline
3. Any differences (changes, deletions, new files) are identified
4. Alerts are generated and logged

---

Project Structure

fim/
├── fim_guard.py
├── config.json
├── requirements.txt
├── README.md

---

Requirements

- Python 3.8 or higher
- Linux system (recommended for monitoring system files)
- Internet access for SMTP email alerts

This project uses only Python standard library modules.

---

Configuration

Edit "config.json" to customize the tool:

{
  "paths": ["/etc/passwd", "/etc/shadow"],
  "log_file": "fim.log",
  "smtp": {
    "server": "smtp.gmail.com",
    "port": 587,
    "username": "your_email@gmail.com",
    "password": "your_password",
    "sender": "your_email@gmail.com",
    "recipient": "your_email@gmail.com"
  }
}

---

Usage

Create Baseline

Run this on a clean, trusted system:

python3 fim_guard.py --baseline

---

Run Integrity Check

python3 fim_guard.py --check

---

Example Output

{
  "timestamp": "2026-04-13T12:00:00Z",
  "changed": ["/etc/passwd"],
  "missing": [],
  "new": ["/etc/malicious_file"]
}

---

Use Case

This tool helps detect:

- Unauthorized modification of system files
- Persistence mechanisms used by attackers
- Privilege escalation attempts
- Suspicious file creation in critical directories

---

Limitations

- Requires baseline to be created on a clean system
- May generate false positives during legitimate system updates
- Depends on proper SMTP configuration for email alerts

---

Skills Demonstrated

- Python scripting and automation
- File integrity monitoring concepts
- Hashing (SHA256)
- Multi-threading
- Security detection and alerting
- SIEM-style log generation

---

Author

Zion
