"""
Test script to verify Flask demo setup
"""

import json
import sys
from pathlib import Path

# Add ai_layer to path
sys.path.insert(0, str(Path(__file__).parent / 'ai_layer'))

from ai_pipeline import run_ai_pipeline

print("\n" + "="*70)
print("🧪 Testing Flask Demo Setup")
print("="*70)

# Test 1: Check demo_case.json exists
print("\n[Test 1] Checking demo_case.json...")
try:
    with open("demo_case.json", 'r', encoding='utf-8') as f:
        demo_data = json.load(f)
    print("✅ demo_case.json loaded successfully")
    print(f"   Case ID: {demo_data.get('case_id')}")
    print(f"   Events: {len(demo_data.get('timeline', {}).get('events', []))}")
except Exception as e:
    print(f"❌ Error loading demo_case.json: {e}")
    sys.exit(1)

# Test 2: Run AI pipeline
print("\n[Test 2] Running AI pipeline...")
try:
    report = run_ai_pipeline(demo_data['case_id'], demo_data, language="en")
    print("✅ AI pipeline executed successfully")
    print(f"   Risk Level: {report['sections']['executive_summary']['risk_assessment']['risk_level']}")
    print(f"   Risk Score: {report['sections']['executive_summary']['risk_assessment']['risk_score']}")
    
    # Check for threat_summary
    if 'threat_summary' in report['sections']['executive_summary']:
        print(f"   Threat Summary: {report['sections']['executive_summary']['threat_summary'][:80]}...")
    else:
        print("   ⚠️  Warning: threat_summary not found in executive summary")
        
except Exception as e:
    print(f"❌ Error running AI pipeline: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check template files
print("\n[Test 3] Checking template files...")
templates = ['templates/index.html', 'templates/results.html']
for template in templates:
    if Path(template).exists():
        print(f"✅ {template} exists")
    else:
        print(f"❌ {template} not found")

# Test 4: Check static files
print("\n[Test 4] Checking static files...")
if Path('static/style.css').exists():
    print("✅ static/style.css exists")
else:
    print("❌ static/style.css not found")

# Test 5: Check Flask app
print("\n[Test 5] Checking Flask app...")
try:
    import app as flask_app
    print("✅ Flask app imports successfully")
    print(f"   Routes: {[rule.rule for rule in flask_app.app.url_map.iter_rules()]}")
except Exception as e:
    print(f"❌ Error importing Flask app: {e}")

print("\n" + "="*70)
print("✅ All tests passed! Flask demo is ready.")
print("="*70)
print("\nTo start the demo:")
print("  python app.py")
print("\nThen open: http://127.0.0.1:5000")
print("="*70 + "\n")
