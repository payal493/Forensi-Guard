"""
AI Intelligence Layer - Integration Demo

This script demonstrates how to integrate the AI Intelligence Layer
with the existing Forensi-Guard forensic engine.

It simulates realistic forensic data and shows the complete pipeline
from forensic output to AI-interpreted report.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ai_pipeline import run_ai_pipeline


def create_realistic_forensic_data():
    """
    Create realistic forensic data structure that matches
    the output from the existing Forensi-Guard forensic engine.
    
    This simulates what your forensic backend (E:\web dev\SVNIT)
    would produce after analyzing a device.
    """
    
    # Base timestamp for timeline
    base_time = datetime.now() - timedelta(days=3)
    
    forensic_data = {
        "case_id": "case_demo_001",
        "metadata": {
            "case_name": "Cyber Harassment Investigation - Demo",
            "investigator": "Officer Demo",
            "device_type": "Android Device (Samsung Galaxy)",
            "acquisition_method": "Logical (ADB)",
            "created_at": datetime.now().isoformat(),
            "device_model": "SM-G991B",
            "android_version": "12",
            "acquisition_date": base_time.isoformat()
        },
        "timeline": {
            "events": [
                {
                    "timestamp": (base_time + timedelta(hours=2)).isoformat(),
                    "source": "app",
                    "details": "Suspicious tracking app installed: com.tracker.stealth",
                    "metadata": {
                        "app": "com.tracker.stealth",
                        "package_name": "com.tracker.stealth",
                        "permissions": ["ACCESS_FINE_LOCATION", "READ_CONTACTS", "READ_SMS"]
                    }
                },
                {
                    "timestamp": (base_time + timedelta(hours=2, minutes=5)).isoformat(),
                    "source": "app",
                    "details": "Location permission granted to tracking app",
                    "metadata": {
                        "app": "com.tracker.stealth",
                        "permission": "ACCESS_FINE_LOCATION",
                        "granted": True
                    }
                },
                {
                    "timestamp": (base_time + timedelta(hours=2, minutes=7)).isoformat(),
                    "source": "app",
                    "details": "Contacts permission granted to tracking app",
                    "metadata": {
                        "app": "com.tracker.stealth",
                        "permission": "READ_CONTACTS",
                        "granted": True
                    }
                },
                {
                    "timestamp": (base_time + timedelta(hours=12)).isoformat(),
                    "source": "sms",
                    "details": "SMS received from unknown number",
                    "metadata": {
                        "sender": "+91XXXXXXXXXX",
                        "address": "+91XXXXXXXXXX",
                        "content": "Your verification code is 123456",
                        "body": "Your verification code is 123456"
                    }
                },
                {
                    "timestamp": (base_time + timedelta(days=1, hours=2)).isoformat(),
                    "source": "call",
                    "details": "Incoming call from unknown number",
                    "metadata": {
                        "number": "+91XXXXXXXXXX",
                        "address": "+91XXXXXXXXXX",
                        "duration": 45,
                        "type": "incoming"
                    }
                },
                {
                    "timestamp": (base_time + timedelta(days=1, hours=14)).isoformat(),
                    "source": "media",
                    "details": "Photo taken with location data",
                    "metadata": {
                        "filename": "IMG_20240115_140000.jpg",
                        "name": "IMG_20240115_140000.jpg",
                        "location": {
                            "latitude": 23.1234,
                            "longitude": 72.5678
                        }
                    }
                },
                {
                    "timestamp": (base_time + timedelta(days=2, hours=1)).isoformat(),
                    "source": "app",
                    "details": "Background location tracking detected",
                    "metadata": {
                        "app": "com.tracker.stealth",
                        "activity": "background_location_access"
                    }
                }
            ]
        },
        "findings": {
            "suspicious_behaviour": [
                {
                    "type": "suspicious_behaviour",
                    "description": "App with hidden icon detected",
                    "severity": "high",
                    "details": {
                        "app": "com.tracker.stealth",
                        "reason": "App launcher icon is hidden from app drawer"
                    }
                },
                {
                    "type": "suspicious_behaviour",
                    "description": "Excessive background location access",
                    "severity": "high",
                    "details": {
                        "app": "com.tracker.stealth",
                        "frequency": "Every 5 minutes",
                        "duration": "48 hours"
                    }
                }
            ],
            "malware_indicators": [
                {
                    "type": "malware",
                    "description": "App matches stalkerware signature",
                    "severity": "critical",
                    "details": {
                        "app": "com.tracker.stealth",
                        "signature_match": "Known stalkerware pattern",
                        "confidence": 0.85
                    }
                }
            ],
            "timestamp_anomalies": [
                {
                    "type": "timestamp_anomaly",
                    "description": "Nighttime device activity detected",
                    "severity": "medium",
                    "details": {
                        "time_range": "01:00 - 03:00 AM",
                        "activity": "Background app activity"
                    }
                }
            ],
            "permission_abuse": [
                {
                    "type": "permission",
                    "description": "App has excessive permissions for its category",
                    "severity": "high",
                    "details": {
                        "app": "com.tracker.stealth",
                        "category": "Utility",
                        "excessive_permissions": [
                            "ACCESS_FINE_LOCATION",
                            "READ_CONTACTS",
                            "READ_SMS"
                        ]
                    }
                }
            ]
        },
        "hashes": {
            "algorithm": "SHA-256",
            "files": [
                {
                    "path": "/data/app/com.tracker.stealth/base.apk",
                    "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
                }
            ]
        }
    }
    
    return forensic_data


def display_report_summary(report):
    """
    Display a human-readable summary of the AI-generated report.
    
    Args:
        report: AI-interpreted report from the pipeline
    """
    print("\n" + "="*70)
    print("📊 AI-INTERPRETED REPORT SUMMARY")
    print("="*70)
    
    # Case information
    print(f"\n📁 Case ID: {report.get('case_id')}")
    print(f"🌐 Language: {report.get('language')}")
    print(f"⏰ Generated: {report.get('generated_at')}")
    
    # Executive Summary
    if "sections" in report and "executive_summary" in report["sections"]:
        exec_summary = report["sections"]["executive_summary"]
        risk = exec_summary.get("risk_assessment", {})
        
        print("\n" + "-"*70)
        print("⚠️  RISK ASSESSMENT")
        print("-"*70)
        print(f"Risk Level: {risk.get('risk_level', 'Unknown')}")
        print(f"Risk Score: {risk.get('risk_score', 0):.1f}/100")
        print(f"Confidence: {risk.get('confidence', 0):.1f}%")
        print(f"\nReasoning: {risk.get('reasoning', 'N/A')}")
        
        # Key findings
        key_findings = exec_summary.get("key_findings", [])
        if key_findings:
            print(f"\n🔍 Key Findings ({len(key_findings)}):")
            for i, finding in enumerate(key_findings[:3], 1):
                print(f"\n{i}. {finding.get('finding', 'N/A')}")
                print(f"   Confidence: {finding.get('confidence', 0):.1f}%")
    
    # Timeline Narrative
    if "sections" in report and "timeline_narrative" in report["sections"]:
        timeline = report["sections"]["timeline_narrative"]
        
        print("\n" + "-"*70)
        print("📖 TIMELINE NARRATIVE")
        print("-"*70)
        print(timeline.get("narrative", "No narrative available"))
        
        # Patterns
        patterns = timeline.get("patterns", [])
        if patterns:
            print(f"\n🔍 Detected Patterns ({len(patterns)}):")
            for pattern in patterns:
                print(f"  • {pattern}")
    
    # Safety Recommendations
    if "sections" in report and "safety_recommendations" in report["sections"]:
        safety = report["sections"]["safety_recommendations"]
        recommendations = safety.get("recommendations", [])
        
        print("\n" + "-"*70)
        print(f"🛡️  SAFETY RECOMMENDATIONS (Priority: {safety.get('priority', 'N/A')})")
        print("-"*70)
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n{i}. [{rec.get('category', 'N/A')}] {rec.get('action', 'N/A')}")
            print(f"   Priority: {rec.get('priority', 'N/A')}")
            print(f"   Reasoning: {rec.get('reasoning', 'N/A')}")
    
    # Metadata
    if "metadata" in report:
        metadata = report["metadata"]
        print("\n" + "-"*70)
        print("📈 PROCESSING METADATA")
        print("-"*70)
        print(f"Processing Time: {metadata.get('processing_time_seconds', 0):.2f} seconds")
        print(f"Average Confidence: {metadata.get('confidence_average', 0):.1f}%")
        print(f"Components Executed: {', '.join(metadata.get('components_executed', []))}")
    
    print("\n" + "="*70 + "\n")


def save_report_to_file(report, filename="ai_report_demo.json"):
    """
    Save the AI report to a JSON file.
    
    Args:
        report: AI-interpreted report
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✅ Report saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving report: {e}")
        return False


def main():
    """
    Main demo function showing complete integration workflow.
    """
    print("\n" + "="*70)
    print("🚀 AI INTELLIGENCE LAYER - INTEGRATION DEMO")
    print("="*70)
    print("\nThis demo shows how to integrate the AI layer with your")
    print("existing Forensi-Guard forensic engine.")
    print("\n" + "="*70)
    
    # Step 1: Create realistic forensic data
    print("\n[Demo Step 1] Creating realistic forensic data...")
    print("(This simulates output from your forensic engine)")
    forensic_data = create_realistic_forensic_data()
    print(f"✅ Created forensic data with {len(forensic_data['timeline']['events'])} events")
    
    # Step 2: Process through AI pipeline
    print("\n[Demo Step 2] Processing through AI Intelligence Layer...")
    case_id = forensic_data["case_id"]
    
    # THIS IS THE KEY INTEGRATION POINT
    # In your actual code, you would call this after forensic analysis:
    report = run_ai_pipeline(case_id, forensic_data, language="en")
    
    # Step 3: Display results
    print("\n[Demo Step 3] Displaying AI-interpreted results...")
    display_report_summary(report)
    
    # Step 4: Save report
    print("\n[Demo Step 4] Saving report to file...")
    save_report_to_file(report)
    
    # Integration guide
    print("\n" + "="*70)
    print("📚 INTEGRATION GUIDE")
    print("="*70)
    print("""
To integrate with your existing forensic backend:

1. In your app.py or generate_report.py:
   
   from ai_layer import run_ai_pipeline
   
2. After forensic analysis completes:
   
   forensic_data = {
       "case_id": case_id,
       "metadata": {...},
       "timeline": {...},
       "findings": {...},
       "hashes": {...}
   }
   
3. Process through AI layer:
   
   ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
   
4. Use the AI report:
   
   # Access risk assessment
   risk = ai_report["sections"]["executive_summary"]["risk_assessment"]
   
   # Access narrative
   narrative = ai_report["sections"]["timeline_narrative"]["narrative"]
   
   # Access recommendations
   recommendations = ai_report["sections"]["safety_recommendations"]
   
5. All AI outputs are marked with "ai_generated": true
   Display this clearly in your UI!

Note: Multilingual support (Hindi, Gujarati) will be added later
      by your teammate. For now, use language="en" only.
    """)
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
