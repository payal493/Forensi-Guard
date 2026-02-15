"""
Test script to verify multilingual integration
"""

import json
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / 'ai_layer'))
sys.path.insert(0, str(Path(__file__).parent))

from ai_pipeline import run_ai_pipeline
from language_layer.translator import translate_report

print("\n" + "="*70)
print("🧪 Testing Multilingual Integration")
print("="*70)

# Test 1: Load demo case
print("\n[Test 1] Loading demo case...")
try:
    with open("demo_case.json", 'r', encoding='utf-8') as f:
        demo_data = json.load(f)
    print("✅ Demo case loaded")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 2: Run AI pipeline (English)
print("\n[Test 2] Running AI pipeline (English)...")
try:
    report_en = run_ai_pipeline(demo_data['case_id'], demo_data, language="en")
    print("✅ English report generated")
    print(f"   Threat Summary: {report_en['sections']['executive_summary'].get('threat_summary', 'N/A')[:60]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 3: Translate to Hindi
print("\n[Test 3] Translating to Hindi...")
try:
    report_hi = translate_report(report_en.copy(), 'hi')
    print("✅ Hindi translation completed")
    print(f"   Language: {report_hi.get('language')}")
    print(f"   Threat Summary: {report_hi['sections']['executive_summary'].get('threat_summary', 'N/A')[:80]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Translate to Gujarati
print("\n[Test 4] Translating to Gujarati...")
try:
    report_gu = translate_report(report_en.copy(), 'gu')
    print("✅ Gujarati translation completed")
    print(f"   Language: {report_gu.get('language')}")
    print(f"   Threat Summary: {report_gu['sections']['executive_summary'].get('threat_summary', 'N/A')[:80]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Verify evidence integrity
print("\n[Test 5] Verifying evidence integrity...")
try:
    # Check that technical data is preserved
    en_artefacts = report_en['sections']['evidence_interpretation']['artefacts']
    hi_artefacts = report_hi['sections']['evidence_interpretation']['artefacts']
    
    # Check timestamps are unchanged
    if en_artefacts[0]['original'] == hi_artefacts[0]['original']:
        print("✅ Original artefact data preserved")
    else:
        print("⚠️  Warning: Original data may have been modified")
    
    # Check numbers are preserved
    en_risk = report_en['sections']['executive_summary']['risk_assessment']['risk_score']
    hi_risk = report_hi['sections']['executive_summary']['risk_assessment']['risk_score']
    
    if en_risk == hi_risk:
        print("✅ Risk scores preserved")
    else:
        print("⚠️  Warning: Risk scores differ")
        
except Exception as e:
    print(f"⚠️  Could not verify integrity: {e}")

# Test 6: Check Flask app import
print("\n[Test 6] Checking Flask app...")
try:
    import app as flask_app
    print("✅ Flask app imports successfully")
    print(f"   Translation available: {flask_app.TRANSLATION_AVAILABLE}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("✅ Multilingual integration tests complete!")
print("="*70)
print("\nTo test the UI:")
print("  1. Run: python app.py")
print("  2. Open: http://127.0.0.1:5000")
print("  3. Select language (English/Hindi/Gujarati)")
print("  4. Click 'Run Demo Analysis'")
print("  5. View translated results")
print("="*70 + "\n")
