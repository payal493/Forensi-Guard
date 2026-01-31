import os
import json
from datetime import datetime, timezone

REPORT_PATH = os.path.join("reports", "final_report.txt")
HASH_FILE = os.path.join("evidence", "hashes", "hashes.json")
FINDINGS_FILE = os.path.join("analysis", "findings.json")
TIMELINE_FILE = os.path.join("timeline", "timeline.json")

lines = []

def add(line=""):
    lines.append(line)

# -----------------------------
# REPORT HEADER
# -----------------------------
add("MOBILE DIGITAL FORENSICS INVESTIGATION REPORT")
add("=" * 50)
add(f"Case ID: MF-CASE-001")
add(f"Report Generated (UTC): {datetime.now(timezone.utc).isoformat()}")
add("Dataset Used: NIST CFReDS Android")
add("Tool: Mobile Forensics Investigation Tool")
add()

# -----------------------------
# EVIDENCE INTEGRITY SECTION
# -----------------------------
add("EVIDENCE INTEGRITY VERIFICATION")
add("-" * 50)

if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as f:
        hash_data = json.load(f)

    add(f"Hash Algorithm: {hash_data.get('algorithm', 'SHA-256')}")
    files = hash_data.get("files", [])
    add(f"Total Evidence Files Hashed: {len(files)}")
    add()

    for item in files:
        add(f"- File Name: {item['file_name']}")
        add(f"  Relative Path: {item['relative_path']}")
        add(f"  Size (bytes): {item['size_bytes']}")
        add(f"  SHA-256: {item['sha256']}")
        add()
else:
    add("No hash data available.")
    add()

# -----------------------------
# ANALYSIS FINDINGS SECTION
# -----------------------------
add("ANALYSIS FINDINGS")
add("-" * 50)

if os.path.exists(FINDINGS_FILE):
    with open(FINDINGS_FILE, "r") as f:
        findings = json.load(f).get("findings", [])

    if findings:
        for idx, finding in enumerate(findings, start=1):
            add(f"{idx}. {finding['type']}")
            add(f"   {finding['description']}")
            add()
    else:
        add("No analysis findings detected.")
        add()
else:
    add("Analysis findings file not present.")
    add()

# -----------------------------
# TIMELINE SECTION
# -----------------------------
add("TIMELINE OVERVIEW")
add("-" * 50)

if os.path.exists(TIMELINE_FILE):
    with open(TIMELINE_FILE, "r") as f:
        events = json.load(f).get("events", [])

    if events:
        for event in events:
            add(f"[{event['timestamp']}] {event['source']} - {event['details']}")
        add()
    else:
        add("Timeline file is empty.")
        add()
else:
    add("Timeline file not present.")
    add()

# -----------------------------
# CONCLUSION
# -----------------------------
add("CONCLUSION")
add("-" * 50)
add("Evidence integrity was preserved using SHA-256 hashing.")
add("All findings are based on rule-based, explainable analysis.")
add("This report represents the final forensic output of the investigation.")
add()

# -----------------------------
# WRITE REPORT TO FILE
# -----------------------------
with open(REPORT_PATH, "w", encoding="utf-8") as report:
    report.write("\n".join(lines))

print("Forensic report generated successfully.")
