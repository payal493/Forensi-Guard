"""
Comprehensive test of the complete Forensi-Guard workflow
Tests: Case Selection → Data Transformation → AI Processing → Translation
"""

import os
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("🧪 FORENSI-GUARD COMPLETE WORKFLOW TEST")
print("="*70)

# Test 1: Import all modules
print("\n[Test 1] Importing modules...")
try:
    from app import get_available_cases, transform_forensic_report_to_ai_format
    from ai_layer.ai_pipeline import run_ai_pipeline
    from language_layer.translator import translate_report
    print("   ✅ All modules imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Get available cases
print("\n[Test 2] Detecting available cases...")
cases = get_available_cases()
print(f"   ✅ Found {len(cases)} cases: {', '.join(cases)}")

if len(cases) == 0:
    print("   ❌ No cases found!")
    sys.exit(1)

# Test 3: Process each case
print("\n[Test 3] Processing all cases...")
CASE_DIR = os.path.join(os.path.dirname(__file__), "mobile-forensics-tool", "cases")

results = []

for case in cases:
    print(f"\n   📁 Processing {case}...")
    
    try:
        # Load forensic report
        report_path = os.path.join(CASE_DIR, case, "reports", "forensic_report.json")
        with open(report_path, 'r', encoding='utf-8') as f:
            forensic_report = json.load(f)
        
        # Transform to AI format
        forensic_data = transform_forensic_report_to_ai_format(forensic_report, case)
        
        # Run AI pipeline
        report = run_ai_pipeline(case, forensic_data, language="en")
        
        if report.get("status") == "error":
            print(f"      ❌ Error: {report.get('error_details')}")
            continue
        
        # Extract results
        exec_summary = report['sections']['executive_summary']
        risk = exec_summary['risk_assessment']
        
        result = {
            "case": case,
            "risk_level": risk['risk_level'],
            "risk_score": risk['risk_score'],
            "threat_summary": exec_summary.get('threat_summary', 'N/A'),
            "findings_count": len(exec_summary.get('key_findings', [])),
            "recommendations_count": len(report['sections']['safety_recommendations']['recommendations'])
        }
        
        results.append(result)
        
        print(f"      ✅ Success!")
        print(f"         Risk: {result['risk_level']} ({result['risk_score']})")
        print(f"         Findings: {result['findings_count']}")
        print(f"         Recommendations: {result['recommendations_count']}")
        
    except Exception as e:
        print(f"      ❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Test 4: Test translation
print("\n[Test 4] Testing multilingual support...")
if len(results) > 0:
    try:
        # Get first case report
        first_case = cases[0]
        report_path = os.path.join(CASE_DIR, first_case, "reports", "forensic_report.json")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            forensic_report = json.load(f)
        
        forensic_data = transform_forensic_report_to_ai_format(forensic_report, first_case)
        report_en = run_ai_pipeline(first_case, forensic_data, language="en")
        
        # Test Hindi translation
        report_hi = translate_report(report_en, "hi")
        print(f"   ✅ Hindi translation: Success")
        
        # Test Gujarati translation
        report_gu = translate_report(report_en, "gu")
        print(f"   ✅ Gujarati translation: Success")
        
        # Verify structure preserved
        assert report_en.keys() == report_hi.keys() == report_gu.keys()
        print(f"   ✅ Report structure preserved across languages")
        
    except Exception as e:
        print(f"   ❌ Translation error: {e}")

# Test 5: Summary
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)

print(f"\nTotal Cases Tested: {len(results)}")
print(f"Successful: {len(results)}")
print(f"Failed: {len(cases) - len(results)}")

if len(results) > 0:
    print("\n📈 Results by Case:")
    for result in results:
        print(f"\n   {result['case']}:")
        print(f"      Risk Level: {result['risk_level']}")
        print(f"      Risk Score: {result['risk_score']}")
        print(f"      Findings: {result['findings_count']}")
        print(f"      Recommendations: {result['recommendations_count']}")
        print(f"      Threat: {result['threat_summary'][:60]}...")

print("\n" + "="*70)
print("✅ COMPLETE WORKFLOW TEST FINISHED")
print("="*70)

print("\n🚀 Ready for demo! Run: python app.py")
print("="*70 + "\n")
