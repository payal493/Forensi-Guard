"""
AI Intelligence Layer - Quick Test Script

Run this to verify the AI pipeline is working correctly.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ai_pipeline import run_ai_pipeline


def test_minimal_case():
    """Test with minimal forensic data."""
    print("\n" + "="*70)
    print("TEST 1: Minimal Forensic Data")
    print("="*70)
    
    minimal_data = {
        "case_id": "test_minimal",
        "metadata": {
            "case_name": "Test Case",
            "investigator": "Test Officer",
            "device_type": "Android",
            "acquisition_method": "Logical (ADB)",
            "created_at": "2024-01-15T10:00:00Z"
        },
        "timeline": {
            "events": []
        },
        "findings": {
            "suspicious_behaviour": [],
            "malware_indicators": [],
            "timestamp_anomalies": [],
            "permission_abuse": []
        },
        "hashes": {
            "algorithm": "SHA-256",
            "files": []
        }
    }
    
    try:
        report = run_ai_pipeline("test_minimal", minimal_data)
        
        if report.get("status") == "error":
            print("❌ Test FAILED:", report.get("error_message"))
            return False
        
        print("✅ Test PASSED: Minimal case processed successfully")
        print(f"   Risk Level: {report['sections']['executive_summary']['risk_assessment']['risk_level']}")
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False


def test_with_findings():
    """Test with forensic findings."""
    print("\n" + "="*70)
    print("TEST 2: Forensic Data with Findings")
    print("="*70)
    
    data_with_findings = {
        "case_id": "test_findings",
        "metadata": {
            "case_name": "Test Case with Findings",
            "investigator": "Test Officer",
            "device_type": "Android",
            "acquisition_method": "Logical (ADB)",
            "created_at": "2024-01-15T10:00:00Z"
        },
        "timeline": {
            "events": [
                {
                    "timestamp": "2024-01-10T14:00:00Z",
                    "source": "app",
                    "details": "Suspicious app installed",
                    "metadata": {
                        "app": "com.test.tracker",
                        "permission": "ACCESS_FINE_LOCATION"
                    }
                }
            ]
        },
        "findings": {
            "suspicious_behaviour": [
                {
                    "type": "suspicious_behaviour",
                    "description": "Unusual background activity",
                    "severity": "high"
                }
            ],
            "malware_indicators": [
                {
                    "type": "malware",
                    "description": "Potential stalkerware detected",
                    "severity": "critical"
                }
            ],
            "timestamp_anomalies": [],
            "permission_abuse": []
        },
        "hashes": {
            "algorithm": "SHA-256",
            "files": []
        }
    }
    
    try:
        report = run_ai_pipeline("test_findings", data_with_findings)
        
        if report.get("status") == "error":
            print("❌ Test FAILED:", report.get("error_message"))
            return False
        
        risk = report['sections']['executive_summary']['risk_assessment']
        print("✅ Test PASSED: Case with findings processed successfully")
        print(f"   Risk Level: {risk['risk_level']}")
        print(f"   Risk Score: {risk['risk_score']:.1f}/100")
        print(f"   Interpretations: {len(report['sections']['evidence_interpretation']['artefacts'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False


def test_timeline_narrative():
    """Test timeline narrative generation."""
    print("\n" + "="*70)
    print("TEST 3: Timeline Narrative Generation")
    print("="*70)
    
    data_with_timeline = {
        "case_id": "test_timeline",
        "metadata": {
            "case_name": "Test Timeline",
            "investigator": "Test Officer",
            "device_type": "Android",
            "acquisition_method": "Logical (ADB)",
            "created_at": "2024-01-15T10:00:00Z"
        },
        "timeline": {
            "events": [
                {
                    "timestamp": "2024-01-10T14:00:00Z",
                    "source": "app",
                    "details": "App installed",
                    "metadata": {}
                },
                {
                    "timestamp": "2024-01-10T14:05:00Z",
                    "source": "app",
                    "details": "Permission granted",
                    "metadata": {}
                },
                {
                    "timestamp": "2024-01-10T15:00:00Z",
                    "source": "sms",
                    "details": "SMS received",
                    "metadata": {}
                }
            ]
        },
        "findings": {},
        "hashes": {
            "algorithm": "SHA-256",
            "files": []
        }
    }
    
    try:
        report = run_ai_pipeline("test_timeline", data_with_timeline)
        
        if report.get("status") == "error":
            print("❌ Test FAILED:", report.get("error_message"))
            return False
        
        narrative = report['sections']['timeline_narrative']
        print("✅ Test PASSED: Timeline narrative generated successfully")
        print(f"   Events processed: {narrative['event_count']}")
        print(f"   Key events identified: {len(narrative['key_events'])}")
        print(f"   Patterns detected: {len(narrative['patterns'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False


def test_recommendations():
    """Test safety recommendations generation."""
    print("\n" + "="*70)
    print("TEST 4: Safety Recommendations Generation")
    print("="*70)
    
    high_risk_data = {
        "case_id": "test_recommendations",
        "metadata": {
            "case_name": "High Risk Test",
            "investigator": "Test Officer",
            "device_type": "Android",
            "acquisition_method": "Logical (ADB)",
            "created_at": "2024-01-15T10:00:00Z"
        },
        "timeline": {
            "events": []
        },
        "findings": {
            "suspicious_behaviour": [
                {"type": "suspicious_behaviour", "severity": "high"}
            ],
            "malware_indicators": [
                {"type": "malware", "severity": "critical"}
            ],
            "timestamp_anomalies": [],
            "permission_abuse": []
        },
        "hashes": {
            "algorithm": "SHA-256",
            "files": []
        }
    }
    
    try:
        report = run_ai_pipeline("test_recommendations", high_risk_data)
        
        if report.get("status") == "error":
            print("❌ Test FAILED:", report.get("error_message"))
            return False
        
        recommendations = report['sections']['safety_recommendations']
        print("✅ Test PASSED: Safety recommendations generated successfully")
        print(f"   Recommendations: {len(recommendations['recommendations'])}")
        print(f"   Priority: {recommendations['priority']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False


def test_output_format():
    """Test output format validation."""
    print("\n" + "="*70)
    print("TEST 5: Output Format Validation")
    print("="*70)
    
    minimal_data = {
        "case_id": "test_format",
        "metadata": {
            "case_name": "Format Test",
            "investigator": "Test Officer",
            "device_type": "Android",
            "acquisition_method": "Logical (ADB)",
            "created_at": "2024-01-15T10:00:00Z"
        },
        "timeline": {"events": []},
        "findings": {},
        "hashes": {"algorithm": "SHA-256", "files": []}
    }
    
    try:
        report = run_ai_pipeline("test_format", minimal_data)
        
        # Check required keys
        required_keys = ["case_id", "language", "generated_at", "sections", "metadata"]
        missing_keys = [key for key in required_keys if key not in report]
        
        if missing_keys:
            print(f"❌ Test FAILED: Missing keys: {missing_keys}")
            return False
        
        # Check sections
        required_sections = [
            "executive_summary",
            "evidence_interpretation",
            "timeline_narrative",
            "safety_recommendations"
        ]
        missing_sections = [s for s in required_sections if s not in report["sections"]]
        
        if missing_sections:
            print(f"❌ Test FAILED: Missing sections: {missing_sections}")
            return False
        
        # Check AI-generated flags
        for section_name, section_data in report["sections"].items():
            if not section_data.get("ai_generated"):
                print(f"❌ Test FAILED: Section '{section_name}' missing 'ai_generated' flag")
                return False
        
        print("✅ Test PASSED: Output format is valid")
        print(f"   All required keys present: {required_keys}")
        print(f"   All required sections present: {required_sections}")
        print(f"   All sections marked as AI-generated: ✓")
        
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*70)
    print("🧪 AI INTELLIGENCE LAYER - TEST SUITE")
    print("="*70)
    print("\nRunning comprehensive tests...\n")
    
    tests = [
        ("Minimal Case", test_minimal_case),
        ("With Findings", test_with_findings),
        ("Timeline Narrative", test_timeline_narrative),
        ("Recommendations", test_recommendations),
        ("Output Format", test_output_format)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! AI Intelligence Layer is working correctly.")
        print("\nNext steps:")
        print("1. Run: python demo_integration.py")
        print("2. Review: flask_integration_example.py")
        print("3. Integrate with your existing forensic backend")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
