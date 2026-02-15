"""
Test script to verify dynamic case selection functionality
"""

import os
import json
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / 'ai_layer'))
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("🧪 Testing Dynamic Case Selection")
print("="*70)

# Test 1: Check case directory
print("\n[Test 1] Checking case directory...")
CASE_DIR = os.path.join(os.path.dirname(__file__), "mobile-forensics-tool", "cases")

if os.path.exists(CASE_DIR):
    print(f"✅ Case directory found: {CASE_DIR}")
else:
    print(f"❌ Case directory not found: {CASE_DIR}")
    sys.exit(1)

# Test 2: Scan for available cases
print("\n[Test 2] Scanning for available cases...")
cases = []

for case in os.listdir(CASE_DIR):
    case_path = os.path.join(CASE_DIR, case)
    
    if not os.path.isdir(case_path):
        continue
    
    report_path = os.path.join(case_path, "reports", "forensic_report.json")
    
    if os.path.exists(report_path):
        cases.append(case)
        print(f"   ✅ Found: {case}")

cases = sorted(cases)
print(f"\n✅ Total cases found: {len(cases)}")

if len(cases) == 0:
    print("❌ No valid cases found!")
    sys.exit(1)

# Test 3: Verify each case has valid JSON
print("\n[Test 3] Verifying forensic reports...")
for case in cases:
    report_path = os.path.join(CASE_DIR, case, "reports", "forensic_report.json")
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"   ✅ {case}: Valid JSON")
    except Exception as e:
        print(f"   ❌ {case}: Invalid JSON - {e}")

# Test 4: Test AI pipeline with first case
print("\n[Test 4] Testing AI pipeline with first case...")
try:
    from ai_pipeline import run_ai_pipeline
    from app import transform_forensic_report_to_ai_format
    
    first_case = cases[0]
    report_path = os.path.join(CASE_DIR, first_case, "reports", "forensic_report.json")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        forensic_report = json.load(f)
    
    # Transform the report to AI pipeline format
    forensic_data = transform_forensic_report_to_ai_format(forensic_report, first_case)
    
    print(f"   Processing: {first_case}")
    report = run_ai_pipeline(first_case, forensic_data, language="en")
    
    if report.get("status") == "error":
        print(f"   ❌ Error: {report.get('error_details')}")
    else:
        print(f"   ✅ AI pipeline executed successfully")
        print(f"   Risk Level: {report['sections']['executive_summary']['risk_assessment']['risk_level']}")
        print(f"   Risk Score: {report['sections']['executive_summary']['risk_assessment']['risk_score']}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test Flask app import
print("\n[Test 5] Testing Flask app...")
try:
    import app as flask_app
    
    # Test get_available_cases function
    available_cases = flask_app.get_available_cases()
    print(f"   ✅ Flask app imports successfully")
    print(f"   Available cases: {available_cases}")
    
    # Test case labels
    print(f"   Case labels defined: {len(flask_app.CASE_LABELS)}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✅ Dynamic case selection tests complete!")
print("="*70)
print("\nTo test the UI:")
print("  1. Run: python app.py")
print("  2. Open: http://127.0.0.1:5000")
print("  3. Select a case from dropdown")
print("  4. Select language")
print("  5. Click 'Run Analysis'")
print("  6. View results with case name displayed")
print("="*70 + "\n")
