#!/usr/bin/env python3
"""
Debug CSV parsing for live debug communication ingestion
"""

import csv
from pathlib import Path

def debug_csv_parsing():
    base_path = Path(__file__).parent.parent
    raw_dir = base_path / "cases" / "case_live_001" / "evidence" / "raw"
    
    call_file = raw_dir / "live_debug_calllog.csv"
    sms_file = raw_dir / "live_debug_sms.csv"
    
    print("🔍 Debugging CSV parsing...")
    
    # Debug call log
    print(f"\n📞 Reading call log: {call_file}")
    with open(call_file, 'r') as f:
        lines = f.readlines()
        print(f"Total lines: {len(lines)}")
        for i, line in enumerate(lines):
            print(f"Line {i}: {repr(line)}")
    
    print(f"\n💬 Reading SMS log: {sms_file}")
    with open(sms_file, 'r') as f:
        lines = f.readlines()
        print(f"Total lines: {len(lines)}")
        for i, line in enumerate(lines):
            print(f"Line {i}: {repr(line)}")
    
    # Test CSV parsing
    print(f"\n🧪 Testing CSV parsing...")
    
    with open(call_file, 'r') as f:
        # Find header
        for line in f:
            if line.startswith('timestamp'):
                print(f"Found header: {line.strip()}")
                break
        
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            print(f"Row {i}: {row}")
            if i >= 3:  # Limit output
                break

if __name__ == "__main__":
    debug_csv_parsing()
