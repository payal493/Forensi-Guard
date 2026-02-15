"""
Flask Integration Example

This file shows how to integrate the AI Intelligence Layer
with your existing Flask-based forensic backend.

DO NOT replace your existing app.py with this file.
Instead, use this as a reference to add AI capabilities.
"""

from flask import Flask, jsonify, request
from ai_layer import run_ai_pipeline
import json

# This is an EXAMPLE - adapt to your existing Flask app
app = Flask(__name__)


# EXAMPLE 1: Add AI interpretation to existing case analysis endpoint
@app.route('/api/analyze_case/<case_id>', methods=['POST'])
def analyze_case_with_ai(case_id):
    """
    Example endpoint that combines forensic analysis with AI interpretation.
    
    This shows how to integrate AI layer with your existing forensic processing.
    """
    try:
        # Step 1: Your existing forensic analysis
        # (This is your existing code - don't change it)
        # forensic_data = run_your_existing_forensic_analysis(case_id)
        
        # For this example, we'll get it from request
        forensic_data = request.get_json()
        
        # Step 2: Add AI interpretation layer
        # THIS IS THE NEW CODE YOU ADD
        ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
        
        # Step 3: Return combined results
        response = {
            "status": "success",
            "case_id": case_id,
            "forensic_data": forensic_data,  # Original forensic results
            "ai_interpretation": ai_report    # AI-interpreted results
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# EXAMPLE 2: Separate endpoint for AI interpretation only
@app.route('/api/ai_interpret/<case_id>', methods=['POST'])
def ai_interpret_only(case_id):
    """
    Example endpoint that only runs AI interpretation on existing forensic data.
    
    Use this if you want to keep forensic analysis and AI interpretation separate.
    """
    try:
        # Get forensic data from request
        forensic_data = request.get_json()
        
        # Run AI interpretation
        ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
        
        return jsonify(ai_report), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# EXAMPLE 3: Get specific AI components
@app.route('/api/ai_risk_assessment/<case_id>', methods=['POST'])
def get_risk_assessment(case_id):
    """
    Example endpoint to get only risk assessment from AI layer.
    """
    try:
        forensic_data = request.get_json()
        ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
        
        # Extract only risk assessment
        risk_assessment = ai_report.get("sections", {}).get("executive_summary", {}).get("risk_assessment", {})
        
        return jsonify({
            "case_id": case_id,
            "risk_assessment": risk_assessment
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/ai_narrative/<case_id>', methods=['POST'])
def get_timeline_narrative(case_id):
    """
    Example endpoint to get only timeline narrative from AI layer.
    """
    try:
        forensic_data = request.get_json()
        ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
        
        # Extract only timeline narrative
        narrative = ai_report.get("sections", {}).get("timeline_narrative", {})
        
        return jsonify({
            "case_id": case_id,
            "timeline_narrative": narrative
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/ai_recommendations/<case_id>', methods=['POST'])
def get_safety_recommendations(case_id):
    """
    Example endpoint to get only safety recommendations from AI layer.
    """
    try:
        forensic_data = request.get_json()
        ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
        
        # Extract only recommendations
        recommendations = ai_report.get("sections", {}).get("safety_recommendations", {})
        
        return jsonify({
            "case_id": case_id,
            "safety_recommendations": recommendations
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# EXAMPLE 4: Integration with your existing report generation
def generate_enhanced_report(case_id, forensic_data):
    """
    Example function showing how to enhance your existing report generation
    with AI interpretation.
    
    Add this to your existing generate_report.py logic.
    """
    # Your existing report generation
    # (Don't change this part)
    forensic_report = {
        "case_id": case_id,
        "metadata": forensic_data.get("metadata", {}),
        "timeline": forensic_data.get("timeline", {}),
        "findings": forensic_data.get("findings", {}),
        "hashes": forensic_data.get("hashes", {})
    }
    
    # NEW: Add AI interpretation
    try:
        ai_interpretation = run_ai_pipeline(case_id, forensic_data, language="en")
        
        # Combine forensic report with AI interpretation
        enhanced_report = {
            "forensic_analysis": forensic_report,
            "ai_interpretation": ai_interpretation,
            "report_type": "enhanced_with_ai",
            "generated_at": ai_interpretation.get("generated_at")
        }
        
        return enhanced_report
        
    except Exception as e:
        # If AI fails, still return forensic report
        print(f"AI interpretation failed: {e}")
        return {
            "forensic_analysis": forensic_report,
            "ai_interpretation": None,
            "report_type": "forensic_only",
            "ai_error": str(e)
        }


# EXAMPLE 5: Batch processing multiple cases
@app.route('/api/batch_ai_interpret', methods=['POST'])
def batch_ai_interpret():
    """
    Example endpoint for batch processing multiple cases through AI layer.
    """
    try:
        cases = request.get_json().get("cases", [])
        results = []
        
        for case_data in cases:
            case_id = case_data.get("case_id")
            forensic_data = case_data.get("forensic_data")
            
            try:
                ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
                results.append({
                    "case_id": case_id,
                    "status": "success",
                    "ai_report": ai_report
                })
            except Exception as e:
                results.append({
                    "case_id": case_id,
                    "status": "error",
                    "error": str(e)
                })
        
        return jsonify({
            "total_cases": len(cases),
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║         Flask Integration Example - AI Intelligence Layer      ║
    ║                                                                ║
    ║  This is an EXAMPLE file showing integration patterns.         ║
    ║  DO NOT replace your existing app.py with this file.           ║
    ║                                                                ║
    ║  Instead, copy the relevant patterns into your existing code.  ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    
    Example endpoints:
    
    POST /api/analyze_case/<case_id>
        - Combines forensic analysis with AI interpretation
        
    POST /api/ai_interpret/<case_id>
        - AI interpretation only
        
    POST /api/ai_risk_assessment/<case_id>
        - Get only risk assessment
        
    POST /api/ai_narrative/<case_id>
        - Get only timeline narrative
        
    POST /api/ai_recommendations/<case_id>
        - Get only safety recommendations
        
    POST /api/batch_ai_interpret
        - Batch process multiple cases
    
    """)
    
    # Run example server
    app.run(debug=True, port=5001)
