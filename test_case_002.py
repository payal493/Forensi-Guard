"""
Test transformer with case_002 which has more detailed data
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import transform_forensic_report_to_ai_format

print("\n" + "="*70)
print("🧪 Testing with Case 002")
print("="*70)

# Load case_002 forensic report
report_path = "mobile-forensics-tool/cases/case_002/reports/forensic_report.json"

print(f"\n[Test 1] Loading: {report_path}")
with open(report_path, 'r', encoding='utf-8') as f:
    forensic_report = json.load(f)

print("✅ Loaded successfully")

# Transform it
print("\n[Test 2] Transforming...")
transformed = transform_forensic_report_to_ai_format(forensic_report, "case_002")

print("✅ Transformed successfully")
print(f"   Malware indicators: {len(transformed['findings']['malware_indicators'])}")
print(f"   Suspicious behaviour: {len(transformed['findings']['suspicious_behaviour'])}")
print(f"   Timestamp anomalies: {len(transformed['findings']['timestamp_anomalies'])}")

# Test with AI pipeline
print("\n[Test 3] Running AI pipeline...")
try:
    from ai_layer.ai_pipeline import run_ai_pipeline
    
    report = run_ai_pipeline("case_002", transformed, language="en")
    
    if report.get("status") == "error":
        print(f"   ❌ Error: {report.get('error_details')}")
    else:
        print("   ✅ Success!")
        exec_summary = report['sections']['executive_summary']
        risk = exec_summary['risk_assessment']
        
        print(f"\n   📊 Results:")
        print(f"   Risk Level: {risk['risk_level']}")
        print(f"   Risk Score: {risk['risk_score']}")
        print(f"   Threat Summary: {exec_summary.get('threat_summary', 'N/A')}")
        print(f"   Key Findings: {len(exec_summary.get('key_findings', []))}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✅ Test complete!")
print("="*70 + "\n")
