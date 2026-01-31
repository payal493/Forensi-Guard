#!/usr/bin/env python3
"""
Mobile Digital Forensics Investigation Tool - Behaviour Analysis Module

FORENSIC IMPORTANCE:
Behavioural analysis helps investigators identify patterns and anomalies
in mobile device usage that may indicate criminal activity, security breaches,
or unusual user behavior. This module uses rule-based analysis to detect:

- Communication patterns with suspicious contacts
- Activity during unusual hours (potential covert operations)
- Excessive frequency of certain activities
- Geographic or temporal anomalies

All analysis is based on deterministic rules, not machine learning,
ensuring explainable and court-defensible results.
"""

import json
import os
from datetime import datetime, time
from pathlib import Path
from collections import defaultdict, Counter


def load_processed_evidence(processed_dir):
    """
    Load processed evidence from the evidence/processed directory.
    
    TODO: Implement proper JSON file loading with error handling
    TODO: Validate evidence data structure and format
    TODO: Handle missing or corrupted evidence files
    
    Args:
        processed_dir: Path to processed evidence directory
        
    Returns:
        dict: Processed evidence data by source type
    """
    evidence_data = {
        "SMS": [],
        "CALL": [],
        "MEDIA": [],
        "APP": []
    }
    
    # TODO: Load actual evidence files from processed directory
    # Placeholder: Check if processed directory exists
    if os.path.exists(processed_dir):
        print(f"Loading evidence from: {processed_dir}")
        
        # Load SMS evidence
        sms_file = os.path.join(processed_dir, "sms.json")
        if os.path.exists(sms_file):
            try:
                with open(sms_file, 'r') as f:
                    evidence_data["SMS"] = json.load(f)
                print(f"Loaded {len(evidence_data['SMS'])} SMS records")
            except Exception as e:
                print(f"Error loading SMS evidence: {e}")
        
        # Load CALL evidence
        calls_file = os.path.join(processed_dir, "calls.json")
        if os.path.exists(calls_file):
            try:
                with open(calls_file, 'r') as f:
                    evidence_data["CALL"] = json.load(f)
                print(f"Loaded {len(evidence_data['CALL'])} call records")
            except Exception as e:
                print(f"Error loading call evidence: {e}")
        
        # Load MEDIA evidence
        media_file = os.path.join(processed_dir, "media.json")
        if os.path.exists(media_file):
            try:
                with open(media_file, 'r') as f:
                    evidence_data["MEDIA"] = json.load(f)
                print(f"Loaded {len(evidence_data['MEDIA'])} media records")
            except Exception as e:
                print(f"Error loading media evidence: {e}")
        
        # Load APP evidence
        apps_file = os.path.join(processed_dir, "apps.json")
        if os.path.exists(apps_file):
            try:
                with open(apps_file, 'r') as f:
                    evidence_data["APP"] = json.load(f)
                print(f"Loaded {len(evidence_data['APP'])} app records")
            except Exception as e:
                print(f"Error loading app evidence: {e}")
        
    else:
        print(f"Processed evidence directory not found: {processed_dir}")
    
    return evidence_data


def analyze_call_patterns(call_evidence):
    """
    Analyze call patterns for suspicious behaviour.
    
    FORENSIC RULES:
    - Excessive calls to single number (potential stalking/harassment)
    - Calls during unusual hours (2 AM - 5 AM)
    - High frequency of short calls (potential coordination)
    
    TODO: Implement threshold configuration
    TODO: Add geographic pattern analysis
    TODO: Implement call duration anomaly detection
    
    Args:
        call_evidence (list): List of call evidence entries
        
    Returns:
        list: Detected behavioural anomalies
    """
    anomalies = []
    
    if not call_evidence:
        print("No call evidence available for analysis")
        return anomalies
    
    # TODO: Implement excessive call detection
    # Placeholder: Count calls by number
    call_counts = defaultdict(int)
    late_night_calls = []
    
    for call in call_evidence:
        # Extract phone number from details (placeholder logic)
        # TODO: Implement proper phone number extraction
        phone_number = "unknown"
        
        call_counts[phone_number] += 1
        
        # Check for late night calls (suspicious activity)
        try:
            call_time = datetime.strptime(call["timestamp"], "%Y-%m-%d %H:%M:%S").time()
            if time(2, 0) <= call_time <= time(5, 0):
                late_night_calls.append(call)
        except ValueError:
            print(f"Invalid timestamp format: {call['timestamp']}")
    
    # TODO: Implement configurable thresholds
    EXCESSIVE_CALL_THRESHOLD = 50  # Placeholder threshold
    
    # Check for excessive calls to single number
    for number, count in call_counts.items():
        if count > EXCESSIVE_CALL_THRESHOLD:
            anomaly = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "CALL",
                "type": "excessive_calls",
                "details": f"{count} calls to {number} (threshold: {EXCESSIVE_CALL_THRESHOLD})"
            }
            anomalies.append(anomaly)
    
    # Check for late night activity
    if len(late_night_calls) > 10:  # Placeholder threshold
        anomaly = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "CALL", 
            "type": "unusual_hours",
            "details": f"{len(late_night_calls)} calls during 2AM-5AM window"
        }
        anomalies.append(anomaly)
    
    return anomalies


def analyze_sms_patterns(sms_evidence):
    """
    Analyze SMS patterns for suspicious behaviour.
    
    FORENSIC RULES:
    - High volume of messages to single contact
    - Messages during unusual hours
    - Repetitive content patterns
    - Suspicious keywords in messages
    
    TODO: Implement keyword analysis
    TODO: Add message frequency analysis
    TODO: Implement content pattern detection
    
    Args:
        sms_evidence (list): List of SMS evidence entries
        
    Returns:
        list: Detected behavioural anomalies
    """
    anomalies = []
    
    if not sms_evidence:
        print("No SMS evidence available for analysis")
        return anomalies
    
    # TODO: Implement message frequency analysis
    # Placeholder: Count messages by contact
    message_counts = defaultdict(int)
    late_night_messages = []
    
    for message in sms_evidence:
        # Extract contact from details (placeholder logic)
        contact = "unknown"
        message_counts[contact] += 1
        
        # Check for late night messages
        try:
            msg_time = datetime.strptime(message["timestamp"], "%Y-%m-%d %H:%M:%S").time()
            if time(1, 0) <= msg_time <= time(4, 0):
                late_night_messages.append(message)
        except ValueError:
            print(f"Invalid timestamp format: {message['timestamp']}")
    
    # TODO: Implement configurable thresholds
    EXCESSIVE_MESSAGE_THRESHOLD = 100  # Placeholder threshold
    
    # Check for excessive messaging
    for contact, count in message_counts.items():
        if count > EXCESSIVE_MESSAGE_THRESHOLD:
            anomaly = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "SMS",
                "type": "excessive_messaging", 
                "details": f"{count} messages to {contact} (threshold: {EXCESSIVE_MESSAGE_THRESHOLD})"
            }
            anomalies.append(anomaly)
    
    return anomalies


def analyze_app_usage(app_evidence):
    """
    Analyze app usage patterns for suspicious behaviour.
    
    FORENSIC RULES:
    - Apps used during unusual hours
    - High frequency usage of specific apps
    - Usage patterns indicating automation or bots
    
    TODO: Implement app category analysis
    TODO: Add usage pattern detection
    TODO: Implement suspicious app identification
    
    Args:
        app_evidence (list): List of app usage evidence entries
        
    Returns:
        list: Detected behavioural anomalies
    """
    anomalies = []
    
    if not app_evidence:
        print("No app evidence available for analysis")
        return anomalies
    
    # TODO: Implement app usage frequency analysis
    # TODO: Implement suspicious app detection
    # TODO: Add usage pattern analysis
    
    # Placeholder: Check for apps used during unusual hours
    unusual_hour_usage = []
    
    for app_event in app_evidence:
        try:
            event_time = datetime.strptime(app_event["timestamp"], "%Y-%m-%d %H:%M:%S").time()
            if time(3, 0) <= event_time <= time(5, 0):
                unusual_hour_usage.append(app_event)
        except ValueError:
            print(f"Invalid timestamp format: {app_event['timestamp']}")
    
    if len(unusual_hour_usage) > 5:  # Placeholder threshold
        anomaly = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "APP",
            "type": "unusual_hours_usage",
            "details": f"{len(unusual_hour_usage)} app events during 3AM-5AM"
        }
        anomalies.append(anomaly)
    
    return anomalies


def generate_behaviour_report(anomalies):
    """
    Generate a comprehensive behaviour analysis report.
    
    TODO: Implement detailed report formatting
    TODO: Add statistical summaries
    TODO: Include confidence scores for findings
    
    Args:
        anomalies (list): List of detected anomalies
        
    Returns:
        dict: Behaviour analysis report
    """
    report = {
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis_type": "behaviour_analysis",
        "total_anomalies": len(anomalies),
        "anomalies_by_source": defaultdict(int),
        "anomalies_by_type": defaultdict(int),
        "findings": anomalies
    }
    
    # Categorize anomalies
    for anomaly in anomalies:
        report["anomalies_by_source"][anomaly["source"]] += 1
        report["anomalies_by_type"][anomaly["type"]] += 1
    
    return report


def save_analysis_report(report, output_file):
    """
    Save behaviour analysis report to file.
    
    TODO: Implement proper file handling with error checking
    TODO: Add report versioning
    TODO: Implement backup mechanisms
    
    Args:
        report (dict): Behaviour analysis report
        output_file (Path): Output file path
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Behaviour analysis report saved to: {output_file}")
    except Exception as e:
        print(f"Error saving report: {e}")


def main():
    """
    Main execution function for behaviour analysis.
    
    This function coordinates the behavioural analysis workflow:
    1. Load processed evidence from evidence/processed/
    2. Apply rule-based analysis to detect suspicious patterns
    3. Generate comprehensive analysis report
    4. Save results for further investigation
    """
    print("Mobile Forensics - Behaviour Analysis")
    print("=" * 40)
    
    # Use case_002 for this pipeline execution
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_path, "cases", "case_002", "evidence", "processed")
    
    # Load processed evidence
    evidence_data = load_processed_evidence(processed_dir)
    
    all_anomalies = []
    
    # Analyze different evidence types
    print("\nAnalyzing call patterns...")
    call_anomalies = analyze_call_patterns(evidence_data["CALL"])
    all_anomalies.extend(call_anomalies)
    
    print("Analyzing SMS patterns...")
    sms_anomalies = analyze_sms_patterns(evidence_data["SMS"])
    all_anomalies.extend(sms_anomalies)
    
    print("Analyzing app usage patterns...")
    app_anomalies = analyze_app_usage(evidence_data["APP"])
    all_anomalies.extend(app_anomalies)
    
    # Generate comprehensive report
    behaviour_report = generate_behaviour_report(all_anomalies)
    
    # Save report
    output_dir = Path(__file__).parent.parent / "analysis"
    output_file = output_dir / "behaviour_analysis_report.json"
    save_analysis_report(behaviour_report, output_file)
    
    print(f"\nBehaviour Analysis Summary:")
    print(f"  Total anomalies detected: {len(all_anomalies)}")
    print(f"  Call anomalies: {len(call_anomalies)}")
    print(f"  SMS anomalies: {len(sms_anomalies)}")
    print(f"  App anomalies: {len(app_anomalies)}")
    print(f"  Report saved to: {output_file}")


if __name__ == "__main__":
    main()
