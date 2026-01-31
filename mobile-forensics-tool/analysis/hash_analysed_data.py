#!/usr/bin/env python3
"""
Hashing Module for Analysed Data (Analysis Integrity)

This hashes analysis outputs to ensure they are not modified
after generation. This is NOT evidence hashing.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime


# -------------------------------
# PATHS
# -------------------------------
BASE_DIR = Path(__file__).parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
OUTPUT_FILE = BASE_DIR / "reports" / "analysis_hashes.json"


# -------------------------------
# HASH FUNCTION
# -------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


# -------------------------------
# MAIN
# -------------------------------
def main():
    print("Hashing analysed data (analysis outputs)")
    print("=" * 50)

    hashes = []

    for report in ANALYSIS_DIR.glob("*_report.json"):
        hash_value = sha256_file(report)
        hashes.append({
            "file": str(report),
            "hash_algorithm": "SHA-256",
            "hash_value": hash_value
        })

    result = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": "Integrity verification of analysis outputs",
        "hashed_files": hashes
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Analysis hashes saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
