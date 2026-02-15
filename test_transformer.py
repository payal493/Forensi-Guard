"""
Test the forensic report transformer
"""

import json
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

from app import transform_forensic_report_to_ai_format

print("\n" + "="*70)
print("🧪 Testing Forensic Report Transformer")
print("="*70)

# Load a forensic report
report_path = "mobile-forensics-tool/cases/case_001/reports/forensic_report.json"

print(f"\n[Test 1] Loading forensic report: {report_path}")
with open(report_path, 'r', encoding='utf-8') as f:
    forensic_report = json.load(f)

print("✅ Loaded successfully")
print(f"   Keys in original report: {list(forensic_report.keys())}")

# Transform it
print("\n[Test 2] Transforming to AI pipeline format...")
transformed = transform_forensic_report_to_ai_format(forensic_report, "case_001")

print("✅ Transformed successfully")
print(f"   Keys in transformed data: {list(transformed.keys())}")

# Check required keys
print("\n[Test 3] Checking required keys...")
required_keys = ["metadata", "timeline", "findings", "hashes"]
for key in required_keys:
    if key in transformed:
        print(f"   ✅ {key}: present")
    else:
        print(f"   ❌ {key}: MISSING")

# Display structure
print("\n[Test 4] Displaying transformed structure...")
print(json.dumps(transformed, indent=2))

# Test with AI pipeline
print("\n[Test 5] Testing with AI pipeline...")
try:
    from ai_layer.ai_pipeline import run_ai_pipeline
    
    report = run_ai_pipeline("case_001", transformed, language="en")
    
    if report.get("status") == "error":
        print(f"   ❌ AI pipeline returned error: {report.get('error_details')}")
    else:
        print("   ✅ AI pipeline executed successfully")
        print(f"   Risk Level: {report['sections']['executive_summary']['risk_assessment']['risk_level']}")
        print(f"   Risk Score: {report['sections']['executive_summary']['risk_assessment']['risk_score']}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✅ Transformer test complete!")
print("="*70 + "\n")
