#!/usr/bin/env python3
"""
Demo: Analysis Tampering Detection

Shows how hash values change when analysis output is modified.
"""

import hashlib
from pathlib import Path


TARGET_FILE = Path(__file__).parent / "behaviour_analysis_report.json"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("Analysis Tampering Demonstration")
    print("=" * 50)

    if not TARGET_FILE.exists():
        print("Target analysis file not found")
        return

    original_hash = sha256_file(TARGET_FILE)
    print(f"Original hash:\n{original_hash}\n")

    print("Tampering with analysis file...")
    with open(TARGET_FILE, "a", encoding="utf-8") as f:
        f.write("\nTAMPERED\n")

    tampered_hash = sha256_file(TARGET_FILE)
    print(f"Hash after tampering:\n{tampered_hash}\n")

    if original_hash != tampered_hash:
        print("✔ Tampering detected: hashes do NOT match")
    else:
        print("✘ Tampering NOT detected (unexpected)")


if __name__ == "__main__":
    main()
