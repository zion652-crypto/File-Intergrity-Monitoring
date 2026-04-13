## File Integrity Monitoring (FIM) Tool

Description
A Python-based file integrity monitoring tool that detects unauthorized changes to critical system files using SHA256 hashing.



Features
- Baseline creation for trusted system state  
- Detection of modified, missing, or new files  
- Monitoring of critical system paths (e.g. /etc/passwd, /etc/shadow)  
- Email alerting on detection of changes  


 How It Works
1. A baseline of file hashes is created on a clean system  
2. The script compares current file states against the baseline  
3. Any differences trigger an alert  



 Example Use Case
Detects unauthorized modification of system files, which may indicate privilege escalation or persistence by an attacker.



 Skills Demonstrated
- Python scripting  
- Hashing (SHA256)  
- File system monitoring  
- Security automation
