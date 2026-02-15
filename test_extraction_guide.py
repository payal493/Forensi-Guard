"""
Test the extraction guide page
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("🧪 Testing Extraction Guide Page")
print("="*70)

# Test 1: Import Flask app
print("\n[Test 1] Importing Flask app...")
try:
    import app as flask_app
    print("   ✅ Flask app imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Check extraction guide route exists
print("\n[Test 2] Checking extraction guide route...")
try:
    with flask_app.app.test_client() as client:
        response = client.get('/extraction-guide')
        
        if response.status_code == 200:
            print("   ✅ Route exists and returns 200 OK")
        else:
            print(f"   ❌ Route returned status code: {response.status_code}")
            
        # Check if response contains expected content
        html = response.data.decode('utf-8')
        
        checks = [
            ("Title present", "How to Extract Read-Only Data" in html),
            ("Purpose section", "read-only device information" in html),
            ("Checklist section", "Before You Begin" in html),
            ("Step 1 present", "Enable Developer Mode" in html),
            ("Step 2 present", "Enable USB Debugging" in html),
            ("Step 3 present", "Install Android Platform Tools" in html),
            ("ADB commands", "adb devices" in html),
            ("Safety notice", "Safety & Privacy Notice" in html),
            ("FAQ section", "Frequently Asked Questions" in html),
            ("Simplified toggle", "I'm not technical" in html),
            ("Upload section", "Upload Files for Analysis" in html),
        ]
        
        print("\n   Content checks:")
        all_passed = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"      {status} {check_name}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("\n   ✅ All content checks passed")
        else:
            print("\n   ⚠️  Some content checks failed")
            
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check template file exists
print("\n[Test 3] Checking template file...")
import os
template_path = "templates/extraction_guide.html"

if os.path.exists(template_path):
    print(f"   ✅ Template file exists: {template_path}")
    
    # Check file size
    file_size = os.path.getsize(template_path)
    print(f"   ✅ Template size: {file_size} bytes")
    
    if file_size > 10000:
        print("   ✅ Template has substantial content")
    else:
        print("   ⚠️  Template seems small")
else:
    print(f"   ❌ Template file not found: {template_path}")

# Test 4: Check home page link
print("\n[Test 4] Checking home page link to extraction guide...")
try:
    with flask_app.app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        if '/extraction-guide' in html:
            print("   ✅ Link to extraction guide found on home page")
        else:
            print("   ❌ Link to extraction guide NOT found on home page")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ Extraction Guide Tests Complete!")
print("="*70)

print("\n📋 Summary:")
print("   - Extraction guide page created")
print("   - Route /extraction-guide added to Flask app")
print("   - Link added to home page")
print("   - Beginner-friendly UI with step-by-step instructions")
print("   - Simplified view toggle for non-technical users")
print("   - Collapsible command sections")
print("   - Copy buttons for commands")
print("   - Safety & privacy notice")
print("   - FAQ section")
print("   - Upload placeholder")

print("\n🚀 To view the page:")
print("   1. Run: python app.py")
print("   2. Open: http://127.0.0.1:5000")
print("   3. Click: 'Extract Data from Your Android Phone' button")
print("   4. Or visit directly: http://127.0.0.1:5000/extraction-guide")

print("\n" + "="*70 + "\n")
