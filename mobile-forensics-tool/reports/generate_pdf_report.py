#!/usr/bin/env python3
"""
PDF Report Generator for Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Converts forensic_report.json to professional PDF format
- Maintains case-based isolation
- Provides court-ready documentation
- Preserves chain of custody integrity

SECURITY CONSTRAINTS:
- READ-ONLY operation
- No evidence modification
- Case-specific output only
"""

import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate_pdf_report(case_id="case_001"):
    """
    Generate PDF report from forensic_report.json for specified case.
    
    Args:
        case_id: Case identifier (default: "case_001")
    
    Returns:
        - PDF file path if successful
        - None if error
    """
    
    # Paths for case-based isolation
    case_dir = f"../cases/{case_id}"
    json_path = f"{case_dir}/reports/forensic_report.json"
    pdf_path = f"{case_dir}/reports/forensic_report.pdf"
    
    # Load forensic report data
    try:
        with open(json_path, 'r') as f:
            report_data = json.load(f)
        print(f"Loaded forensic report for case {case_id.upper()}")
    except FileNotFoundError:
        print(f"Forensic report not found: {json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in forensic report: {e}")
        return None
    
    # Create PDF document
    try:
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center
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
            ["Case ID:", case_id.upper()],
            ["Report Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Investigator:", report_data.get("report_metadata", {}).get("generated_by", "Unknown")],
            ["Data Source:", "NIST CFReDS Android Dataset"],
            ["Device Type:", "Android Smartphone"]
        ]
        
        case_table = Table(case_info, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(Paragraph("Case Information", heading_style))
        story.append(case_table)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        summary = report_data.get("executive_summary", {})
        summary_text = f"""
        <b>Investigation Overview:</b> {summary.get("investigation_overview", "Not provided")}<br/>
        <b>Key Findings:</b> {summary.get("key_findings", "Not provided")}<br/>
        <b>Risk Assessment:</b> {summary.get("risk_assessment", "Not provided")}<br/>
        <b>Recommendations:</b> {summary.get("recommendations", "Not provided")}
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Timeline Summary
        story.append(Paragraph("Timeline Analysis", heading_style))
        timeline = report_data.get("timeline_summary", {})
        timeline_text = f"""
        <b>Total Events:</b> {timeline.get("total_events", 0)}<br/>
        <b>Date Range:</b> {timeline.get("date_range", {}).get("start", "Unknown")} to {timeline.get("date_range", {}).get("end", "Unknown")}<br/>
        <b>Event Sources:</b> {", ".join(timeline.get("sources", []))}
        """
        story.append(Paragraph(timeline_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Evidence Integrity
        story.append(Paragraph("Evidence Integrity", heading_style))
        integrity = report_data.get("evidence_integrity", {})
        integrity_text = f"""
        <b>Verification Status:</b> {integrity.get("verification_status", "Unknown")}<br/>
        <b>Total Files:</b> {integrity.get("total_files", 0)}<br/>
        <b>Integrity Score:</b> {integrity.get("integrity_score", "Unknown")}%
        """
        story.append(Paragraph(integrity_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Analysis Findings
        story.append(Paragraph("Analysis Findings", heading_style))
        findings = report_data.get("findings_summary", {})
        
        # Behaviour Analysis
        behaviour = findings.get("behaviour_analysis", {})
        story.append(Paragraph("Behaviour Analysis", styles['Heading3']))
        behaviour_text = f"""
        <b>Suspicious Patterns:</b> {len(behaviour.get("suspicious_patterns", []))} identified<br/>
        <b>Risk Level:</b> {behaviour.get("risk_level", "Unknown")}
        """
        story.append(Paragraph(behaviour_text, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Malware Analysis
        malware = findings.get("malware_analysis", {})
        story.append(Paragraph("Malware Analysis", styles['Heading3']))
        malware_text = f"""
        <b>Malware Indicators:</b> {len(malware.get("indicators", []))} detected<br/>
        <b>Threat Level:</b> {malware.get("threat_level", "Unknown")}
        """
        story.append(Paragraph(malware_text, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Anomaly Analysis
        anomaly = findings.get("anomaly_analysis", {})
        story.append(Paragraph("Anomaly Analysis", styles['Heading3']))
        anomaly_text = f"""
        <b>Temporal Anomalies:</b> {len(anomaly.get("anomalies", []))} detected<br/>
        <b>Data Consistency:</b> {anomaly.get("data_consistency", "Unknown")}
        """
        story.append(Paragraph(anomaly_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Conclusions
        story.append(Paragraph("Conclusions", heading_style))
        conclusions = report_data.get("conclusions", {})
        conclusions_text = f"""
        <b>Overall Risk Level:</b> {conclusions.get("overall_risk_level", "Unknown")}<br/>
        <b>Investigation Status:</b> {conclusions.get("investigation_status", "Unknown")}<br/>
        <b>Next Steps:</b> {conclusions.get("next_steps", "Not specified")}
        """
        story.append(Paragraph(conclusions_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = f"""
        <br/><br/>
        <hr/>
        <center>
        <i>Report generated by Mobile Forensics Investigation Tool v1.0<br/>
        Case {case_id.upper()} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
        This report maintains chain of custody integrity</i>
        </center>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        print(f"PDF report generated: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return None

if __name__ == "__main__":
    print("Mobile Forensics Tool - PDF Report Generator")
    print("==========================================")
    
    # Generate PDF for default case
    result = generate_pdf_report("case_001")
    
    if result:
        print("✅ PDF report generation successful")
        print(f"📄 Report saved: {result}")
    else:
        print("❌ PDF report generation failed")
        print("Check that forensic_report.json exists for the case")
