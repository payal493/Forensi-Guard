"""
Flask integration example for the Multilingual Safety Summary Generator
"""

from flask import Flask, request, jsonify
from safety_generator import SafetySummaryGenerator

app = Flask(__name__)
safety_generator = SafetySummaryGenerator()

@app.route('/api/safety-summary', methods=['POST'])
def generate_safety_summary():
    """
    API endpoint to generate multilingual safety summaries.
    
    Expected JSON payload:
    {
        "risk_level": "HIGH|MEDIUM|LOW",
        "issue_type": "location_tracking|suspicious_permissions|background_tracking|stalkerware_indicators",
        "reasoning": "Technical reasoning from forensic analysis",
        "confidence": 0.87
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        required_fields = ['risk_level', 'issue_type', 'reasoning', 'confidence']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = safety_generator.generate_safety_summary(
            risk_level=data['risk_level'],
            issue_type=data['issue_type'],
            reasoning=data['reasoning'],
            confidence=data['confidence']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/supported-issues', methods=['GET'])
def get_supported_issues():
    """Get list of supported issue types."""
    return jsonify({"supported_issues": safety_generator.get_supported_issue_types()})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Forensi-Guard Safety Summary Generator"})

@app.route('/api/add-translation', methods=['POST'])
def add_custom_translation():
    """
    Add custom translation for new issue types.
    
    Expected JSON payload:
    {
        "issue_type": "new_issue_type",
        "risk_level": "HIGH|MEDIUM|LOW",
        "translations": {
            "english": "English message",
            "hindi": "हिंदी संदेश",
            "gujarati": "ગુજરાતી સંદેશ"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        required_fields = ['issue_type', 'risk_level', 'translations']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        safety_generator.add_custom_translation(
            issue_type=data['issue_type'],
            risk_level=data['risk_level'],
            translations_dict=data['translations']
        )
        
        return jsonify({"message": "Custom translation added successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Forensi-Guard Safety Summary Generator API...")
    print("Available endpoints:")
    print("  POST /api/safety-summary - Generate safety summary")
    print("  GET  /api/supported-issues - Get supported issue types")
    print("  GET  /api/health - Health check")
    print("  POST /api/add-translation - Add custom translation")
    print("\nExample usage:")
    print("curl -X POST http://localhost:5000/api/safety-summary \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"risk_level\":\"HIGH\",\"issue_type\":\"location_tracking\",\"reasoning\":\"App tracks location\",\"confidence\":0.87}'")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
