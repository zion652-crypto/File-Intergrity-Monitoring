#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import logging
import smtplib
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from email.message import EmailMessage

# ---------------- CONFIG ----------------

CONFIG_FILE = Path("config.json")
BASELINE_FILE = Path("baseline.json")

# ---------------- LOAD CONFIG ----------------

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

# ---------------- LOGGING ----------------

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

# ---------------- HASHING ----------------

def sha256_file(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return path, h.hexdigest()
    except Exception as e:
        return path, None

# ---------------- FILE COLLECTION ----------------

def collect_targets(paths):
    targets = set()
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for name in files:
                    targets.add(os.path.join(root, name))
        elif os.path.isfile(p):
            targets.add(p)
    return list(targets)

# ---------------- SNAPSHOT ----------------

def snapshot(files):
    data = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(sha256_file, files)

    for path, file_hash in results:
        try:
            stat = os.stat(path)
            data[path] = {
                "hash": file_hash,
                "size": stat.st_size,
                "mtime": int(stat.st_mtime)
            }
        except:
            data[path] = {"error": "stat failed"}

    return data

# ---------------- EMAIL ----------------

def send_email(config, subject, message):
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = config["smtp"]["sender"]
        msg["To"] = config["smtp"]["recipient"]

        with smtplib.SMTP(config["smtp"]["server"], config["smtp"]["port"]) as server:
            server.starttls()
            server.login(config["smtp"]["username"], config["smtp"]["password"])
            server.send_message(msg)

        logging.info("Email sent")
    except Exception as e:
        logging.error(f"Email failed: {e}")

# ---------------- BASELINE ----------------

def create_baseline(config):
    logging.info("Creating baseline")
    files = collect_targets(config["paths"])
    data = {
        "created": datetime.utcnow().isoformat() + "Z",
        "files": snapshot(files)
    }
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    logging.info("Baseline created")

# ---------------- CHECK ----------------

def check_integrity(config):
    if not BASELINE_FILE.exists():
        print("Run baseline first.")
        return

    baseline = json.load(open(BASELINE_FILE))["files"]
    current = snapshot(collect_targets(config["paths"]))

    changed, missing, new = [], [], []

    for f in baseline:
        if f not in current:
            missing.append(f)
        elif baseline[f].get("hash") != current[f].get("hash"):
            changed.append(f)

    for f in current:
        if f not in baseline:
            new.append(f)

    if changed or missing or new:
        alert = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "changed": changed,
            "missing": missing,
            "new": new
        }

        logging.warning("Integrity violation detected")

        # Save SIEM-style alert
        with open("alerts.json", "a") as f:
            f.write(json.dumps(alert) + "\n")

        # Send email
        send_email(config, "FIM ALERT", json.dumps(alert, indent=2))

        print(json.dumps(alert, indent=2))
    else:
        logging.info("No issues found")
        print("No integrity issues.")

# ---------------- MAIN ----------------

def main():
    parser = argparse.ArgumentParser(description="FIM Tool")
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--check", action="store_true")

    args = parser.parse_args()

    config = load_config()
    setup_logging(config["log_file"])

    if args.baseline:
        create_baseline(config)
    elif args.check:
        check_integrity(config)
    else:
        parser.print_help()

if _name_ == "_main_":
    main()
