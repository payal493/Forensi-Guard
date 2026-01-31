#!/usr/bin/env python3
"""
Mobile Digital Forensics Investigation Tool
Anomaly Analysis for Call Logs

Detects temporal and logical inconsistencies in call data.
"""

import json
from datetime import datetime, time
from pathlib import Path


# -------------------------------
# CONFIGURATION
# -------------------------------
PROCESSED_DIR = Path(__file__).parent.parent / "evidence" / "processed"
OUTPUT_FILE = Path(__file__).parent.parent / "analysis" / "anomaly_call_analysis_report.json"

TIME_GAP_HOURS = 24


# -------------------------------
# DATA LOADING
# -------------------------------
def load_calls():
    calls_file = PROCESSED_DIR / "calls.json"

    if not calls_file.exists():
        print("No calls.json found")
        return []

    with open(calls_file, "r", encoding="utf-8") as f:
        calls = json.load(f)

    print(f"Loaded {len(calls)} call records")
    return calls


# -------------------------------
# ANOMALY RULES
# -------------------------------
def detect_call_anomalies(calls):
    findings = []

    if len(calls) < 2:
        return findings

    # Sort calls by timestamp
    calls_sorted = sorted(
        calls,
        key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")
    )

    # Rule 1: Large time gaps
    for i in range(1, len(calls_sorted)):
        t1 = datetime.strptime(
            calls_sorted[i - 1]["timestamp"], "%Y-%m-%d %H:%M:%S"
        )
        t2 = datetime.strptime(
            calls_sorted[i]["timestamp"], "%Y-%m-%d %H:%M:%S"
        )

        gap_hours = (t2 - t1).total_seconds() / 3600

        if gap_hours >= TIME_GAP_HOURS:
            findings.append({
                "timestamp": calls_sorted[i]["timestamp"],
                "source": "CALL",
                "type": "temporal_gap",
                "details": f"Unusual time gap of {int(gap_hours)} hours between calls"
            })

    # Rule 2: Calls during unusual hours
    for call in calls:
        call_time = datetime.strptime(
            call["timestamp"], "%Y-%m-%d %H:%M:%S"
        ).time()

        if time(0, 0) <= call_time <= time(4, 0):
            findings.append({
                "timestamp": call["timestamp"],
                "source": "CALL",
                "type": "unusual_hour",
                "details": "Call activity detected during unusual hours (00:00–04:00)"
            })

    return findings


# -------------------------------
# REPORT
# -------------------------------
def save_report(findings):
    report = {
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis_type": "anomaly_call_analysis",
        "total_anomalies": len(findings),
        "findings": findings
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Anomaly call analysis report saved to: {OUTPUT_FILE}")


# -------------------------------
# MAIN
# -------------------------------
def main():
    print("Mobile Forensics - Anomaly Call Analysis")
    print("=" * 40)

    calls = load_calls()
    findings = detect_call_anomalies(calls)

    save_report(findings)

    print("\nAnomaly Call Analysis Summary:")
    print(f"  Total anomalies detected: {len(findings)}")
    print(f"  Report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
