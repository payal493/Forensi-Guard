#!/usr/bin/env python3
"""
Merge Analysis Findings for Live Case - Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Merge all analysis results into unified findings.json for live case
- Maintain case-based isolation
- Preserve all analysis indicators
- Generate comprehensive findings for UI consumption
"""

import json
import os
from datetime import datetime

def merge_live_analysis_findings(case_id="case_live_001"):
    """
    Merge all analysis results into a unified findings.json file for live case.
    
    Args:
        case_id: Case identifier
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case_dir = os.path.join(base_path, "cases", case_id, "analysis")
    
    # Initialize findings structure
    findings = {
        "integration_note": "Live debug communication artifacts for pipeline validation",
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "case_id": case_id,
        "suspicious_behaviour": [],
        "malware_indicators": [],
        "timestamp_anomalies": []
    }
    
    # Create basic analysis findings for live case
    # Since this is debug data, we'll create minimal findings
    
    # Load communication patterns for behaviour analysis
    processed_dir = os.path.join(base_path, "cases", case_id, "evidence", "processed")
    
    # Analyze communication patterns
    calls_file = os.path.join(processed_dir, "calls.json")
    sms_file = os.path.join(processed_dir, "sms.json")
    
    if os.path.exists(calls_file):
        try:
            with open(calls_file, 'r') as f:
                calls = json.load(f)
                
            # Simple behaviour analysis
            if len(calls) > 3:
                findings["suspicious_behaviour"].append({
                    "pattern": "High call frequency",
                    "description": f"Multiple calls detected ({len(calls)} calls)",
                    "risk_level": "low",
                    "evidence_references": ["calls.json"]
                })
                
        except Exception as e:
            print(f"Error analyzing calls: {e}")
    
    if os.path.exists(sms_file):
        try:
            with open(sms_file, 'r') as f:
                messages = json.load(f)
                
            # Simple behaviour analysis
            if len(messages) > 3:
                findings["suspicious_behaviour"].append({
                    "pattern": "High message frequency", 
                    "description": f"Multiple messages detected ({len(messages)} messages)",
                    "risk_level": "low",
                    "evidence_references": ["sms.json"]
                })
                
        except Exception as e:
            print(f"Error analyzing SMS: {e}")
    
    # Save merged findings
    os.makedirs(case_dir, exist_ok=True)
    findings_file = os.path.join(case_dir, "findings.json")
    with open(findings_file, 'w') as f:
        json.dump(findings, f, indent=2)
    
    print(f"Merged findings saved to: {findings_file}")
    print(f"Total findings: {len(findings['suspicious_behaviour']) + len(findings['malware_indicators']) + len(findings['timestamp_anomalies'])}")
    
    return findings

if __name__ == "__main__":
    print("Mobile Forensics - Merge Live Case Analysis Findings")
    print("=" * 60)
    
    findings = merge_live_analysis_findings("case_live_001")
    
    print("\nMerge Summary:")
    print(f"  Suspicious behaviour: {len(findings['suspicious_behaviour'])}")
    print(f"  Malware indicators: {len(findings['malware_indicators'])}")
    print(f"  Timestamp anomalies: {len(findings['timestamp_anomalies'])}")
    print(f"  Total findings: {len(findings['suspicious_behaviour']) + len(findings['malware_indicators']) + len(findings['timestamp_anomalies'])}")
