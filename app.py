"""
Forensi-Guard Demo UI
Minimal Flask interface for AI-assisted forensic analysis demonstration
"""

from flask import Flask, render_template, jsonify, request
import json
import sys
import os
from pathlib import Path

# Add ai_layer to path
sys.path.insert(0, str(Path(__file__).parent / 'ai_layer'))

from ai_pipeline import run_ai_pipeline

# Import translation module
try:
    from language_layer.translator import translate_report
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("⚠️  Warning: Translation module not available. Only English will be supported.")

app = Flask(__name__)

# Case directory path
CASE_DIR = os.path.join(os.path.dirname(__file__), "mobile-forensics-tool", "cases")

# Friendly case labels (optional)
CASE_LABELS = {
    "demo_case": "🔴 Demo Case - Suspicious Surveillance Activity (High Risk)",
    "case_001": "Case 001 - General Investigation",
    "case_002": "Case 002 - Suspicious Activity",
    "case_003": "Case 003 - Device Analysis",
    "case_004": "Case 004 - Evidence Review"
}


def get_available_cases():
    """
    Auto-detect available forensic cases.
    
    Returns:
        list: Sorted list of case folder names that have valid forensic reports
    """
    cases = []
    
    # Always add demo case first
    cases.append("demo_case")
    
    if not os.path.exists(CASE_DIR):
        print(f"⚠️  Warning: Case directory not found: {CASE_DIR}")
        return cases
    
    try:
        for case in os.listdir(CASE_DIR):
            case_path = os.path.join(CASE_DIR, case)
            
            # Skip if not a directory
            if not os.path.isdir(case_path):
                continue
            
            # Check if forensic_report.json exists
            report_path = os.path.join(case_path, "reports", "forensic_report.json")
            
            if os.path.exists(report_path):
                cases.append(case)
        
        return cases
    
    except Exception as e:
        print(f"⚠️  Error scanning cases: {e}")
        return cases


def transform_forensic_report_to_ai_format(forensic_report: dict, case_id: str) -> dict:
    """
    Transform forensic report structure to AI pipeline expected format.
    
    Converts from mobile-forensics-tool report format to AI pipeline format.
    Extracts meaningful data from summary reports and creates structured findings.
    
    Args:
        forensic_report: Original forensic report from mobile-forensics-tool
        case_id: Case identifier
    
    Returns:
        dict: Transformed data in AI pipeline expected format
    """
    # Extract metadata
    case_metadata = forensic_report.get("case_metadata", {})
    report_metadata = forensic_report.get("report_metadata", {})
    
    # Build metadata section
    metadata = {
        "case_name": case_metadata.get("case_name", f"Case {case_id}"),
        "investigator": case_metadata.get("investigator", report_metadata.get("investigator", "Unknown")),
        "device_type": case_metadata.get("device_type", "Mobile Device"),
        "acquisition_method": "Forensic Extraction",
        "created_at": case_metadata.get("created_at", report_metadata.get("generation_timestamp", "")),
        "device_model": case_metadata.get("device_model", "Unknown"),
        "case_status": case_metadata.get("case_status", "Active")
    }
    
    # Build timeline section
    timeline_summary = forensic_report.get("timeline_summary", {})
    timeline = {
        "events": [],  # Detailed events not available in summary reports
        "summary": {
            "total_events": timeline_summary.get("total_events", 0),
            "date_range": timeline_summary.get("date_range", {}),
            "sources": timeline_summary.get("sources", timeline_summary.get("sources_summary", {}))
        }
    }
    
    # Build findings section from analysis_findings
    analysis_findings = forensic_report.get("analysis_findings", {})
    findings = {
        "malware_indicators": [],
        "suspicious_behaviour": [],
        "timestamp_anomalies": analysis_findings.get("timestamp_anomalies", []),
        "permission_abuse": []
    }
    
    # Extract structured findings from analysis
    behaviour_analysis = analysis_findings.get("behaviour_analysis", {})
    if behaviour_analysis:
        risk_level = behaviour_analysis.get("risk_level", "low")
        suspicious_count = behaviour_analysis.get("suspicious_patterns", 0)
        
        if suspicious_count > 0:
            findings["suspicious_behaviour"].append({
                "type": "suspicious_behaviour",
                "description": f"Suspicious behaviour patterns detected ({suspicious_count} patterns)",
                "severity": risk_level,
                "details": behaviour_analysis
            })
    
    malware_analysis = analysis_findings.get("malware_analysis", {})
    if malware_analysis:
        risk_level = malware_analysis.get("risk_level", "low")
        malware_count = malware_analysis.get("malware_indicators", 0)
        
        if malware_count > 0:
            findings["malware_indicators"].append({
                "type": "malware",
                "description": f"Malware indicators detected ({malware_count} indicators)",
                "severity": risk_level,
                "details": malware_analysis
            })
    
    anomaly_analysis = analysis_findings.get("anomaly_analysis", {})
    if anomaly_analysis:
        risk_level = anomaly_analysis.get("risk_level", "low")
        anomaly_count = anomaly_analysis.get("temporal_anomalies", 0)
        
        if anomaly_count > 0 and not findings["timestamp_anomalies"]:
            # Add as finding if not already in timestamp_anomalies
            findings["suspicious_behaviour"].append({
                "type": "temporal_anomaly",
                "description": f"Temporal anomalies detected ({anomaly_count} anomalies)",
                "severity": risk_level,
                "details": anomaly_analysis
            })
    
    # Extract findings from conclusions if available
    conclusions = forensic_report.get("conclusions", {})
    if conclusions:
        key_findings = conclusions.get("key_findings", [])
        overall_risk = conclusions.get("overall_risk_level", "LOW")
        
        # Convert key findings to structured findings
        for finding_text in key_findings:
            # Determine severity based on overall risk
            severity = "medium" if overall_risk.upper() in ["MEDIUM", "SUSPICIOUS"] else "low"
            if overall_risk.upper() in ["HIGH", "CRITICAL"]:
                severity = "high"
            
            # Categorize finding based on keywords
            finding_lower = finding_text.lower()
            if any(word in finding_lower for word in ["malware", "virus", "trojan", "spyware"]):
                findings["malware_indicators"].append({
                    "type": "malware",
                    "description": finding_text,
                    "severity": severity,
                    "source": "forensic_analysis"
                })
            elif any(word in finding_lower for word in ["permission", "access", "privilege"]):
                findings["permission_abuse"].append({
                    "type": "permission",
                    "description": finding_text,
                    "severity": severity,
                    "source": "forensic_analysis"
                })
            else:
                findings["suspicious_behaviour"].append({
                    "type": "suspicious_behaviour",
                    "description": finding_text,
                    "severity": severity,
                    "source": "forensic_analysis"
                })
    
    # Build hashes section
    evidence_integrity = forensic_report.get("evidence_integrity", {})
    hashes = {
        "algorithm": evidence_integrity.get("hash_algorithm", "SHA-256"),
        "verification_status": evidence_integrity.get("hash_verification_status", "UNKNOWN"),
        "total_files_hashed": evidence_integrity.get("total_files_hashed", 0),
        "integrity_score": evidence_integrity.get("integrity_score", 0),
        "files": []  # Detailed file hashes not in summary report
    }
    
    # Construct final format
    transformed_data = {
        "case_id": case_id,
        "metadata": metadata,
        "timeline": timeline,
        "findings": findings,
        "hashes": hashes,
        "original_report": {
            "conclusions": conclusions,
            "suspicion_classification": forensic_report.get("suspicion_classification", {})
        }
    }
    
    return transformed_data


@app.route('/')
def index():
    """Home page with case selection"""
    cases = get_available_cases()
    
    # Create case options with labels
    case_options = []
    for case in cases:
        label = CASE_LABELS.get(case, case)
        case_options.append({"value": case, "label": label})
    
    return render_template('index.html', cases=case_options)


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Run AI analysis on selected forensic case
    
    Returns:
        JSON response with analysis results or error
    """
    try:
        # Get selected case and language from form
        selected_case = request.form.get('case')
        language = request.form.get('language', 'en')
        
        # Validate inputs
        if not selected_case:
            return jsonify({
                "status": "error",
                "message": "No case selected"
            }), 400
        
        if language not in ['en', 'hi', 'gu']:
            language = 'en'
        
        # Handle demo case specially
        if selected_case == "demo_case":
            # Load demo case data directly
            demo_case_path = os.path.join(os.path.dirname(__file__), "demo_case.json")
            
            if not os.path.exists(demo_case_path):
                return jsonify({
                    "status": "error",
                    "message": "Demo case file not found"
                }), 404
            
            with open(demo_case_path, 'r', encoding='utf-8') as f:
                forensic_data = json.load(f)
            
            case_id = forensic_data.get("case_id", "demo_case_001")
            case_label = CASE_LABELS.get("demo_case", "Demo Case")
        
        else:
            # Handle regular forensic cases
            # Build path to forensic report
            report_path = os.path.join(
                CASE_DIR,
                selected_case,
                "reports",
                "forensic_report.json"
            )
            
            # Check if report exists
            if not os.path.exists(report_path):
                return jsonify({
                    "status": "error",
                    "message": f"Forensic report not found for case: {selected_case}"
                }), 404
            
            # Load forensic data
            with open(report_path, 'r', encoding='utf-8') as f:
                forensic_report = json.load(f)
            
            # Transform forensic report to AI pipeline expected format
            forensic_data = transform_forensic_report_to_ai_format(forensic_report, selected_case)
            
            # Extract case ID
            case_id = forensic_data.get("case_id", selected_case)
            case_label = CASE_LABELS.get(selected_case, selected_case)
        
        # Run AI pipeline (always in English first)
        report = run_ai_pipeline(case_id, forensic_data, language="en")
        
        # Translate if language is not English
        if language != 'en' and TRANSLATION_AVAILABLE:
            try:
                report = translate_report(report, language)
            except Exception as e:
                print(f"⚠️  Translation failed: {e}. Falling back to English.")
                language = 'en'  # Fallback to English
        
        # Return success response
        return jsonify({
            "status": "success",
            "report": report,
            "language": language,
            "case_name": selected_case,
            "case_label": case_label,
            "is_demo": selected_case == "demo_case"
        })
        
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": f"File not found: {str(e)}"
        }), 404
        
    except json.JSONDecodeError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid JSON in forensic report: {str(e)}"
        }), 500
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Analysis failed: {str(e)}"
        }), 500


@app.route('/results')
def results():
    """Results display page"""
    return render_template('results.html')


@app.route('/extraction-guide')
def extraction_guide():
    """Android data extraction guide page"""
    return render_template('extraction_guide.html')


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Forensi-Guard Demo UI Starting...")
    print("="*70)
    print("\n📍 Open your browser and navigate to: http://127.0.0.1:5000")
    print("\n⚠️  This is a DEMO interface for prototype demonstration only.")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
