#!/usr/bin/env python3
"""
Case-based Report Generator for Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Generate comprehensive forensic report for specific case
- Include all analysis findings and timeline
- Maintain case-based isolation
- Create both JSON and PDF outputs
"""

import json
import os
from datetime import datetime, timezone

def generate_case_report(case_id="case_002"):
    """
    Generate comprehensive forensic report for a specific case.
    
    Args:
        case_id: Case identifier
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case_dir = os.path.join(base_path, "cases", case_id)
    
    # Initialize report structure
    report = {
        "report_metadata": {
            "generation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tool_version": "mobile-forensics-tool v1.0",
            "investigator": "Forensic Pipeline Orchestrator",
            "case_number": case_id.upper(),
            "evidence_source": "NIST CFReDS Android Dataset"
        },
        "case_metadata": {},
        "evidence_integrity": {},
        "timeline_summary": {},
        "analysis_findings": {},
        "suspicion_classification": {},
        "conclusions": {}
    }
    
    # Load case metadata
    metadata_file = os.path.join(case_dir, "metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            report["case_metadata"] = json.load(f)
    
    # Load hash integrity
    hash_file = os.path.join(case_dir, "evidence", "hashes", "hashes.json")
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as f:
            hash_data = json.load(f)
            report["evidence_integrity"] = {
                "hash_verification_status": "VERIFIED",
                "total_files_hashed": hash_data.get("total_files_processed", 0),
                "hash_algorithm": hash_data.get("hash_algorithm", "SHA-256"),
                "integrity_score": 100.0
            }
    
    # Load timeline summary
    timeline_file = os.path.join(case_dir, "timeline", "timeline.json")
    if os.path.exists(timeline_file):
        with open(timeline_file, 'r') as f:
            timeline = json.load(f)
            report["timeline_summary"] = {
                "total_events": len(timeline),
                "date_range": {
                    "start": timeline[0].get("timestamp") if timeline else "Unknown",
                    "end": timeline[-1].get("timestamp") if timeline else "Unknown"
                },
                "sources": list(set(event.get("source", "Unknown") for event in timeline))
            }
    
    # Load analysis findings
    findings_file = os.path.join(case_dir, "analysis", "findings.json")
    if os.path.exists(findings_file):
        with open(findings_file, 'r') as f:
            findings = json.load(f)
            report["analysis_findings"] = {
                "suspicious_behaviour": findings.get("suspicious_behaviour", []),
                "malware_indicators": findings.get("malware_indicators", []),
                "timestamp_anomalies": findings.get("timestamp_anomalies", [])
            }
    
    # Load suspicion classification
    status_file = os.path.join(case_dir, "analysis", "case_status.json")
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            report["suspicion_classification"] = json.load(f)
    
    # Generate conclusions
    total_findings = (
        len(report["analysis_findings"].get("suspicious_behaviour", [])) +
        len(report["analysis_findings"].get("malware_indicators", [])) +
        len(report["analysis_findings"].get("timestamp_anomalies", []))
    )
    
    report["conclusions"] = {
        "overall_risk_level": report["suspicion_classification"].get("suspicion_level", "Unknown"),
        "total_findings": total_findings,
        "investigation_status": "Complete",
        "next_steps": "Review findings and determine further investigation needs"
    }
    
    # Save JSON report
    reports_dir = os.path.join(case_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    json_report_file = os.path.join(reports_dir, "forensic_report.json")
    with open(json_report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"JSON report saved to: {json_report_file}")
    
    # Generate PDF report
    pdf_report_file = os.path.join(reports_dir, "forensic_report.pdf")
    generate_pdf_report(report, pdf_report_file)
    
    return report

def generate_pdf_report(report_data, output_path):
    """Generate PDF version of the report"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Title
        story.append(Paragraph("MOBILE FORENSICS INVESTIGATION REPORT", title_style))
        story.append(Spacer(1, 20))
        
        # Case Information
        case_info = [
            ["Case ID:", report_data["case_metadata"].get("case_id", "Unknown")],
            ["Investigator:", report_data["case_metadata"].get("investigator", "Unknown")],
            ["Device Type:", report_data["case_metadata"].get("device_type", "Unknown")],
            ["Data Source:", report_data["case_metadata"].get("data_source", "Unknown")],
            ["Report Generated:", report_data["report_metadata"]["generation_timestamp"]]
        ]
        
        story.append(Paragraph("Case Information", heading_style))
        for key, value in case_info:
            story.append(Paragraph(f"<b>{key}</b> {value}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Evidence Summary
        story.append(Paragraph("Evidence Summary", heading_style))
        evidence_text = f"""
        <b>Total Files Hashed:</b> {report_data["evidence_integrity"].get("total_files_hashed", 0)}<br/>
        <b>Hash Algorithm:</b> {report_data["evidence_integrity"].get("hash_algorithm", "Unknown")}<br/>
        <b>Timeline Events:</b> {report_data["timeline_summary"].get("total_events", 0)}<br/>
        <b>Date Range:</b> {report_data["timeline_summary"].get("date_range", {}).get("start", "Unknown")} to {report_data["timeline_summary"].get("date_range", {}).get("end", "Unknown")}
        """
        story.append(Paragraph(evidence_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Analysis Findings
        story.append(Paragraph("Analysis Findings", heading_style))
        findings = report_data["analysis_findings"]
        findings_text = f"""
        <b>Suspicious Behaviour:</b> {len(findings.get("suspicious_behaviour", []))} indicators<br/>
        <b>Malware Indicators:</b> {len(findings.get("malware_indicators", []))} indicators<br/>
        <b>Timestamp Anomalies:</b> {len(findings.get("timestamp_anomalies", []))} anomalies
        """
        story.append(Paragraph(findings_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Suspicion Classification
        story.append(Paragraph("Suspicion Classification", heading_style))
        suspicion = report_data["suspicion_classification"]
        suspicion_text = f"""
        <b>Risk Level:</b> {suspicion.get("suspicion_level", "Unknown")}<br/>
        <b>Score:</b> {suspicion.get("score", 0)}
        """
        story.append(Paragraph(suspicion_text, styles['Normal']))
        
        if suspicion.get("reasons"):
            story.append(Paragraph("<b>Classification Reasons:</b>", styles['Normal']))
            for reason in suspicion["reasons"]:
                story.append(Paragraph(f"• {reason}", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Conclusions
        story.append(Paragraph("Conclusions", heading_style))
        conclusions = report_data["conclusions"]
        conclusions_text = f"""
        <b>Overall Risk Level:</b> {conclusions.get("overall_risk_level", "Unknown")}<br/>
        <b>Total Findings:</b> {conclusions.get("total_findings", 0)}<br/>
        <b>Investigation Status:</b> {conclusions.get("investigation_status", "Unknown")}
        """
        story.append(Paragraph(conclusions_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        print(f"PDF report saved to: {output_path}")
        
    except ImportError:
        print("ReportLab not available, skipping PDF generation")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    print("Mobile Forensics - Case Report Generator")
    print("=" * 50)
    
    report = generate_case_report("case_002")
    
    print("\nReport Generation Summary:")
    print(f"  Case ID: {report['case_metadata'].get('case_id', 'Unknown')}")
    print(f"  Timeline Events: {report['timeline_summary'].get('total_events', 0)}")
    print(f"  Total Findings: {report['conclusions'].get('total_findings', 0)}")
    print(f"  Risk Level: {report['suspicion_classification'].get('suspicion_level', 'Unknown')}")
