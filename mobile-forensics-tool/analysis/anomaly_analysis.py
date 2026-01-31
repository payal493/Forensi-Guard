#!/usr/bin/env python3
"""
Mobile Digital Forensics Investigation Tool - Anomaly Analysis Module

FORENSIC IMPORTANCE:
Anomaly analysis in mobile forensics identifies temporal and logical inconsistencies
that may indicate evidence tampering, data manipulation, or suspicious activity.
This module focuses on explainable anomalies that can be clearly demonstrated
in court proceedings:

- Timestamp gaps and inconsistencies
- Events occurring after supposed deletion
- Logical sequence violations
- Temporal ordering anomalies
- Data integrity inconsistencies

All anomaly detection is based on deterministic rules and logical analysis,
ensuring reproducible and defensible forensic findings.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter


def load_processed_evidence(processed_dir):
    """
    Load processed evidence for anomaly analysis.
    
    TODO: Implement proper JSON file loading with validation
    TODO: Add evidence timestamp normalization
    TODO: Handle missing or corrupted evidence files
    
    Args:
        processed_dir: Path to processed evidence directory
        
    Returns:
        dict: Processed evidence data with timestamps
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
        print(f"Loading evidence for anomaly analysis: {processed_dir}")
        
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


def normalize_timestamps(evidence_data):
    """
    Normalize and validate timestamps across all evidence types.
    
    FORENSIC IMPORTANCE:
    Consistent timestamp formatting is essential for temporal analysis.
    Invalid or inconsistent timestamps can indicate manipulation.
    
    TODO: Implement multiple timestamp format support
    TODO: Add timezone normalization
    TODO: Implement timestamp validation rules
    
    Args:
        evidence_data (dict): Raw evidence data
        
    Returns:
        dict: Evidence with normalized timestamps
    """
    normalized_data = {}
    
    for source_type, evidence_list in evidence_data.items():
        normalized_evidence = []
        
        for evidence in evidence_list:
            try:
                # Parse timestamp to validate format
                timestamp_str = evidence["timestamp"]
                parsed_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                
                # Add parsed timestamp for easier analysis
                normalized_item = evidence.copy()
                normalized_item["parsed_timestamp"] = parsed_timestamp
                normalized_item["timestamp_valid"] = True
                
            except (ValueError, KeyError) as e:
                print(f"Invalid timestamp in evidence: {evidence.get('timestamp', 'missing')}")
                # Mark as invalid but keep for analysis
                normalized_item = evidence.copy()
                normalized_item["timestamp_valid"] = False
                normalized_item["parsed_timestamp"] = None
            
            normalized_evidence.append(normalized_item)
        
        normalized_data[source_type] = normalized_evidence
    
    return normalized_data


def detect_timestamp_gaps(evidence_data):
    """
    Detect unusual gaps in timestamp sequences.
    
    FORENSIC RULES:
    - Large gaps (>24 hours) may indicate missing data
    - Gaps during active periods are suspicious
    - Consistent gap patterns may indicate systematic deletion
    
    TODO: Implement configurable gap thresholds
    TODO: Add context-aware gap analysis
    TODO: Implement gap pattern recognition
    
    Args:
        evidence_data (dict): Evidence with normalized timestamps
        
    Returns:
        list: Detected timestamp gap anomalies
    """
    anomalies = []
    
    for source_type, evidence_list in evidence_data.items():
        # Filter evidence with valid timestamps
        valid_evidence = [e for e in evidence_list if e.get("timestamp_valid", False)]
        
        if len(valid_evidence) < 2:
            continue
        
        # Sort by timestamp
        valid_evidence.sort(key=lambda x: x["parsed_timestamp"])
        
        # Check for gaps between consecutive events
        for i in range(1, len(valid_evidence)):
            prev_event = valid_evidence[i-1]
            curr_event = valid_evidence[i]
            
            time_diff = curr_event["parsed_timestamp"] - prev_event["parsed_timestamp"]
            
            # TODO: Implement configurable gap threshold
            GAP_THRESHOLD_HOURS = 24  # Placeholder threshold
            
            if time_diff.total_seconds() > GAP_THRESHOLD_HOURS * 3600:
                anomaly = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_type,
                    "type": "timestamp_gap",
                    "details": f"Gap of {time_diff.days} days detected between {prev_event['timestamp']} and {curr_event['timestamp']}"
                }
                anomalies.append(anomaly)
    
    return anomalies


def detect_post_deletion_activity(evidence_data):
    """
    Detect events occurring after supposed deletion.
    
    FORENSIC RULES:
    - Activity after deletion indicates potential data recovery
    - May indicate evidence tampering or system inconsistency
    - Critical for establishing timeline integrity
    
    TODO: Implement deletion event detection
    TODO: Add activity correlation analysis
    TODO: Implement deletion verification
    
    Args:
        evidence_data (dict): Evidence with normalized timestamps
        
    Returns:
        list: Detected post-deletion activity anomalies
    """
    anomalies = []
    
    for source_type, evidence_list in evidence_data.items():
        # Sort by timestamp
        evidence_list.sort(key=lambda x: x.get("parsed_timestamp", datetime.min))
        
        # Track deletion events
        deletion_timestamps = []
        
        for evidence in evidence_list:
            if evidence.get("type") == "deleted" and evidence.get("timestamp_valid"):
                deletion_timestamps.append(evidence["parsed_timestamp"])
        
        # Check for activity after each deletion
        for deletion_time in deletion_timestamps:
            post_deletion_activity = []
            
            for evidence in evidence_list:
                if (evidence.get("timestamp_valid") and 
                    evidence["parsed_timestamp"] > deletion_time and
                    evidence.get("type") != "deleted"):
                    post_deletion_activity.append(evidence)
            
            if post_deletion_activity:
                anomaly = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_type,
                    "type": "post_deletion_activity",
                    "details": f"{len(post_deletion_activity)} events detected after deletion at {deletion_time.strftime('%Y-%m-%d %H:%M:%S')}"
                }
                anomalies.append(anomaly)
    
    return anomalies


def detect_temporal_inconsistencies(evidence_data):
    """
    Detect temporal and logical inconsistencies.
    
    FORENSIC RULES:
    - Events with timestamps in the future (relative to last known activity)
    - Inconsistent sequences (e.g., response before request)
    - Overlapping events that shouldn't overlap
    - Timestamps outside device operational period
    
    TODO: Implement device-specific timeline validation
    TODO: Add logical sequence verification
    TODO: Implement overlapping event detection
    
    Args:
        evidence_data (dict): Evidence with normalized timestamps
        
    Returns:
        list: Detected temporal inconsistency anomalies
    """
    anomalies = []
    
    # Get current time for future timestamp detection
    current_time = datetime.now()
    
    for source_type, evidence_list in evidence_data.items():
        valid_evidence = [e for e in evidence_list if e.get("timestamp_valid", False)]
        
        for evidence in valid_evidence:
            event_time = evidence["parsed_timestamp"]
            
            # Check for future timestamps
            if event_time > current_time:
                anomaly = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_type,
                    "type": "future_timestamp",
                    "details": f"Event timestamp {evidence['timestamp']} is in the future"
                }
                anomalies.append(anomaly)
            
            # TODO: Implement more temporal consistency checks
            # TODO: Check for logical sequence violations
            # TODO: Detect overlapping incompatible events
    
    return anomalies


def detect_data_inconsistencies(evidence_data):
    """
    Detect data integrity and consistency anomalies.
    
    FORENSIC RULES:
    - Duplicate events with identical timestamps
    - Missing mandatory fields in evidence
    - Inconsistent data formats
    - Logical contradictions in evidence
    
    TODO: Implement data format validation
    TODO: Add duplicate detection with tolerance
    TODO: Implement logical consistency checks
    
    Args:
        evidence_data (dict): Evidence data
        
    Returns:
        list: Detected data inconsistency anomalies
    """
    anomalies = []
    
    for source_type, evidence_list in evidence_data.items():
        # Check for duplicate events
        event_signatures = Counter()
        
        for evidence in evidence_list:
            # Create event signature for duplicate detection
            signature = f"{evidence.get('timestamp', '')}_{evidence.get('type', '')}_{evidence.get('details', '')}"
            event_signatures[signature] += 1
            
            # Check for missing mandatory fields
            required_fields = ["timestamp", "source", "type", "details"]
            missing_fields = [field for field in required_fields if field not in evidence]
            
            if missing_fields:
                anomaly = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_type,
                    "type": "missing_fields",
                    "details": f"Missing required fields: {missing_fields} in event {evidence.get('timestamp', 'unknown')}"
                }
                anomalies.append(anomaly)
        
        # Report duplicates
        for signature, count in event_signatures.items():
            if count > 1:
                anomaly = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_type,
                    "type": "duplicate_event",
                    "details": f"Duplicate event detected {count} times: {signature[:50]}..."
                }
                anomalies.append(anomaly)
    
    return anomalies


def calculate_anomaly_severity(anomalies):
    """
    Calculate severity scores for detected anomalies.
    
    FORENSIC METHODOLOGY:
    Severity assessment helps prioritize investigation resources.
    Critical anomalies may indicate evidence tampering.
    
    TODO: Implement weighted severity scoring
    TODO: Add context-aware severity adjustment
    TODO: Implement severity categorization
    
    Args:
        anomalies (list): List of detected anomalies
        
    Returns:
        dict: Severity assessment results
    """
    severity_scores = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }
    
    # TODO: Implement proper severity weighting
    # Placeholder: Simple severity classification
    severity_weights = {
        "future_timestamp": "CRITICAL",
        "post_deletion_activity": "HIGH",
        "timestamp_gap": "MEDIUM",
        "duplicate_event": "LOW",
        "missing_fields": "MEDIUM"
    }
    
    for anomaly in anomalies:
        anomaly_type = anomaly.get("type", "unknown")
        severity = severity_weights.get(anomaly_type, "LOW")
        severity_scores[severity] += 1
    
    return {
        "severity_distribution": severity_scores,
        "total_anomalies": len(anomalies),
        "critical_anomalies": severity_scores["CRITICAL"],
        "high_anomalies": severity_scores["HIGH"]
    }


def generate_anomaly_report(anomalies, severity_assessment):
    """
    Generate comprehensive anomaly analysis report.
    
    TODO: Implement detailed report formatting
    TODO: Add timeline visualization data
    TODO: Include investigation recommendations
    
    Args:
        anomalies (list): Detected anomalies
        severity_assessment (dict): Severity assessment results
        
    Returns:
        dict: Anomaly analysis report
    """
    report = {
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis_type": "anomaly_analysis",
        "severity_assessment": severity_assessment,
        "total_anomalies": len(anomalies),
        "anomalies_by_type": defaultdict(int),
        "anomalies_by_source": defaultdict(int),
        "findings": anomalies
    }
    
    # Categorize anomalies
    for anomaly in anomalies:
        report["anomalies_by_type"][anomaly["type"]] += 1
        report["anomalies_by_source"][anomaly["source"]] += 1
    
    return report


def save_anomaly_report(report, output_file):
    """
    Save anomaly analysis report to file.
    
    TODO: Implement secure file handling
    TODO: Add report integrity verification
    TODO: Implement backup mechanisms
    
    Args:
        report (dict): Anomaly analysis report
        output_file (Path): Output file path
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Anomaly analysis report saved to: {output_file}")
    except Exception as e:
        print(f"Error saving anomaly report: {e}")


def main():
    """
    Main execution function for anomaly analysis.
    
    This function coordinates the anomaly analysis workflow:
    1. Load processed evidence from evidence/processed/
    2. Normalize and validate timestamps
    3. Detect various types of anomalies
    4. Assess severity and impact
    5. Generate comprehensive analysis report
    """
    print("Mobile Forensics - Anomaly Analysis")
    print("=" * 40)
    
    # Use case_002 for this pipeline execution
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_path, "cases", "case_002", "evidence", "processed")
    
    # Load processed evidence
    evidence_data = load_processed_evidence(processed_dir)
    
    # Normalize timestamps
    print("\nNormalizing timestamps...")
    normalized_data = normalize_timestamps(evidence_data)
    
    all_anomalies = []
    
    # Detect different types of anomalies
    print("Detecting timestamp gaps...")
    gap_anomalies = detect_timestamp_gaps(normalized_data)
    all_anomalies.extend(gap_anomalies)
    
    print("Detecting post-deletion activity...")
    deletion_anomalies = detect_post_deletion_activity(normalized_data)
    all_anomalies.extend(deletion_anomalies)
    
    print("Detecting temporal inconsistencies...")
    temporal_anomalies = detect_temporal_inconsistencies(normalized_data)
    all_anomalies.extend(temporal_anomalies)
    
    print("Detecting data inconsistencies...")
    data_anomalies = detect_data_inconsistencies(normalized_data)
    all_anomalies.extend(data_anomalies)
    
    # Calculate severity assessment
    severity_assessment = calculate_anomaly_severity(all_anomalies)
    
    # Generate comprehensive report
    anomaly_report = generate_anomaly_report(all_anomalies, severity_assessment)
    
    # Save report
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_path, "cases", "case_002", "analysis")
    output_file = os.path.join(output_dir, "anomaly_analysis_report.json")
    save_anomaly_report(anomaly_report, output_file)
    
    print(f"\nAnomaly Analysis Summary:")
    print(f"  Total anomalies: {len(all_anomalies)}")
    print(f"  Critical: {severity_assessment['critical_anomalies']}")
    print(f"  High: {severity_assessment['high_anomalies']}")
    print(f"  Timestamp gaps: {len(gap_anomalies)}")
    print(f"  Post-deletion activity: {len(deletion_anomalies)}")
    print(f"  Temporal inconsistencies: {len(temporal_anomalies)}")
    print(f"  Data inconsistencies: {len(data_anomalies)}")
    print(f"  Report saved to: {output_file}")


if __name__ == "__main__":
    main()
