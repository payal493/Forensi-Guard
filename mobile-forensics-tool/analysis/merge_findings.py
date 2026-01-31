#!/usr/bin/env python3
"""
Merge Analysis Findings for Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Merge all analysis results into unified findings.json
- Maintain case-based isolation
- Preserve all analysis indicators
- Generate comprehensive findings for UI consumption
"""

import json
import os
from datetime import datetime

def merge_analysis_findings(case_id="case_002"):
    """
    Merge all analysis results into a unified findings.json file.
    
    Args:
        case_id: Case identifier
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case_dir = os.path.join(base_path, "cases", case_id, "analysis")
    
    # Initialize findings structure
    findings = {
        "integration_note": "Real forensic data from NIST CFReDS Android dataset",
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "case_id": case_id,
        "suspicious_behaviour": [],
        "malware_indicators": [],
        "timestamp_anomalies": []
    }
    
    # Load behaviour analysis
    behaviour_file = os.path.join(case_dir, "behaviour_analysis_report.json")
    if os.path.exists(behaviour_file):
        try:
            with open(behaviour_file, 'r') as f:
                behaviour_data = json.load(f)
                findings["suspicious_behaviour"] = behaviour_data.get("findings", [])
                print(f"Loaded {len(findings['suspicious_behaviour'])} behaviour findings")
        except Exception as e:
            print(f"Error loading behaviour analysis: {e}")
    
    # Load malware analysis
    malware_file = os.path.join(case_dir, "malware_analysis_report.json")
    if os.path.exists(malware_file):
        try:
            with open(malware_file, 'r') as f:
                malware_data = json.load(f)
                findings["malware_indicators"] = malware_data.get("findings", [])
                print(f"Loaded {len(findings['malware_indicators'])} malware indicators")
        except Exception as e:
            print(f"Error loading malware analysis: {e}")
    
    # Load anomaly analysis
    anomaly_file = os.path.join(case_dir, "anomaly_analysis_report.json")
    if os.path.exists(anomaly_file):
        try:
            with open(anomaly_file, 'r') as f:
                anomaly_data = json.load(f)
                findings["timestamp_anomalies"] = anomaly_data.get("findings", [])
                print(f"Loaded {len(findings['timestamp_anomalies'])} timestamp anomalies")
        except Exception as e:
            print(f"Error loading anomaly analysis: {e}")
    
    # Save merged findings
    findings_file = os.path.join(case_dir, "findings.json")
    with open(findings_file, 'w') as f:
        json.dump(findings, f, indent=2)
    
    print(f"Merged findings saved to: {findings_file}")
    print(f"Total findings: {len(findings['suspicious_behaviour']) + len(findings['malware_indicators']) + len(findings['timestamp_anomalies'])}")
    
    return findings

if __name__ == "__main__":
    print("Mobile Forensics - Merge Analysis Findings")
    print("=" * 50)
    
    findings = merge_analysis_findings("case_002")
    
    print("\nMerge Summary:")
    print(f"  Suspicious behaviour: {len(findings['suspicious_behaviour'])}")
    print(f"  Malware indicators: {len(findings['malware_indicators'])}")
    print(f"  Timestamp anomalies: {len(findings['timestamp_anomalies'])}")
    print(f"  Total findings: {len(findings['suspicious_behaviour']) + len(findings['malware_indicators']) + len(findings['timestamp_anomalies'])}")
