# AI Intelligence Layer - Integration Guide

## Quick Integration (3 Steps)

### Step 1: Import the AI Layer

In your existing `app.py` or `generate_report.py`:

```python
from ai_layer import run_ai_pipeline
```

### Step 2: Prepare Forensic Data

Your existing forensic engine should produce data in this format:

```python
forensic_data = {
    "case_id": "case_001",
    "metadata": {
        "case_name": "Investigation Name",
        "investigator": "Officer Name",
        "device_type": "Android Device",
        "acquisition_method": "Logical (ADB)",
        "created_at": "2024-01-15T10:30:00Z"
    },
    "timeline": {
        "events": [
            {
                "timestamp": "2024-01-10T14:23:00Z",
                "source": "app",  # or "sms", "call", "media"
                "details": "Event description",
                "metadata": {}
            }
        ]
    },
    "findings": {
        "suspicious_behaviour": [],
        "malware_indicators": [],
        "timestamp_anomalies": [],
        "permission_abuse": []
    },
    "hashes": {
        "algorithm": "SHA-256",
        "files": []
    }
}
```

### Step 3: Process Through AI Layer

```python
# Run AI interpretation
ai_report = run_ai_pipeline(case_id, forensic_data, language="en")

# Access the results
risk_level = ai_report["sections"]["executive_summary"]["risk_assessment"]["risk_level"]
narrative = ai_report["sections"]["timeline_narrative"]["narrative"]
recommendations = ai_report["sections"]["safety_recommendations"]["recommendations"]
```

## Complete Example

```python
from flask import Flask, jsonify
from ai_layer import run_ai_pipeline

app = Flask(__name__)

@app.route('/analyze/<case_id>')
def analyze_case(case_id):
    # Your existing forensic analysis
    forensic_data = run_your_forensic_analysis(case_id)
    
    # Add AI interpretation
    ai_report = run_ai_pipeline(case_id, forensic_data, language="en")
    
    # Return combined results
    return jsonify({
        "forensic_data": forensic_data,
        "ai_interpretation": ai_report
    })
```

## Output Structure

The AI layer returns a structured report:

```json
{
  "case_id": "case_001",
  "language": "en",
  "generated_at": "2024-01-15T10:30:00Z",
  "sections": {
    "executive_summary": {
      "risk_assessment": {
        "risk_level": "High",
        "risk_score": 72.5,
        "confidence": 88.0,
        "reasoning": "Multiple indicators suggest..."
      },
      "key_findings": [...]
    },
    "evidence_interpretation": {
      "artefacts": [
        {
          "interpretation": "Plain language explanation",
          "confidence": 85.0,
          "reasoning": "Why this interpretation was made",
          "ai_generated": true
        }
      ]
    },
    "timeline_narrative": {
      "narrative": "Chronological story...",
      "key_events": [...],
      "patterns": [...],
      "ai_generated": true
    },
    "safety_recommendations": {
      "recommendations": [
        {
          "category": "Immediate Action",
          "priority": "High",
          "action": "What to do",
          "reasoning": "Why this is recommended",
          "steps": [...]
        }
      ],
      "disclaimer": "Advisory notice...",
      "ai_generated": true
    }
  },
  "metadata": {
    "processing_time_seconds": 2.5,
    "confidence_average": 82.0
  }
}
```

## Accessing Specific Components

### Risk Assessment Only

```python
ai_report = run_ai_pipeline(case_id, forensic_data)
risk = ai_report["sections"]["executive_summary"]["risk_assessment"]

print(f"Risk Level: {risk['risk_level']}")
print(f"Risk Score: {risk['risk_score']}/100")
print(f"Reasoning: {risk['reasoning']}")
```

### Timeline Narrative Only

```python
ai_report = run_ai_pipeline(case_id, forensic_data)
timeline = ai_report["sections"]["timeline_narrative"]

print(f"Narrative: {timeline['narrative']}")
print(f"Key Events: {len(timeline['key_events'])}")
print(f"Patterns: {timeline['patterns']}")
```

### Safety Recommendations Only

```python
ai_report = run_ai_pipeline(case_id, forensic_data)
safety = ai_report["sections"]["safety_recommendations"]

for rec in safety["recommendations"]:
    print(f"[{rec['priority']}] {rec['action']}")
    print(f"Reasoning: {rec['reasoning']}")
```

## Error Handling

The AI layer handles errors gracefully:

```python
try:
    ai_report = run_ai_pipeline(case_id, forensic_data)
    
    if ai_report.get("status") == "error":
        # AI processing failed, but you still have forensic data
        print(f"AI Error: {ai_report.get('error_message')}")
        # Fall back to forensic data only
    else:
        # Success - use AI interpretation
        pass
        
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
    # Fall back to forensic data only
```

## Important Notes

### 1. Read-Only Operation
The AI layer **NEVER** modifies your forensic data:
- All operations are read-only
- Original evidence is preserved
- AI outputs are separate from forensic data

### 2. AI-Generated Labels
All AI outputs include `"ai_generated": true`:
```python
if section.get("ai_generated"):
    # Display "AI-Generated" label in UI
    print("⚠️ AI-Generated Content")
```

### 3. Language Support
Currently only English is supported:
```python
# Use this for now
ai_report = run_ai_pipeline(case_id, forensic_data, language="en")

# Hindi and Gujarati will be added later by your teammate
# ai_report = run_ai_pipeline(case_id, forensic_data, language="hi")
# ai_report = run_ai_pipeline(case_id, forensic_data, language="gu")
```

### 4. Mock AI Logic
Current implementation uses rule-based logic:
- **Evidence Interpretation**: Pattern matching on permissions and content
- **Risk Scoring**: Weighted algorithm based on finding severity
- **Timeline Narration**: Template-based text generation
- **Recommendations**: Context-aware rule-based advice

Future versions will use:
- Local LLM (Llama 2 7B / Mistral 7B)
- Advanced NLG models
- ML-based confidence scoring

## Testing Your Integration

### 1. Run the Demo

```bash
cd ai_layer
python demo_integration.py
```

This creates realistic forensic data and shows the complete pipeline.

### 2. Test with Your Data

```python
# Load your actual forensic data
import json
with open('path/to/your/forensic_output.json') as f:
    forensic_data = json.load(f)

# Process through AI layer
from ai_layer import run_ai_pipeline
ai_report = run_ai_pipeline(forensic_data["case_id"], forensic_data)

# Save AI report
with open('ai_report.json', 'w') as f:
    json.dump(ai_report, f, indent=2)
```

### 3. Check Flask Integration

See `flask_integration_example.py` for complete Flask examples.

## Performance

Current performance (mock AI logic):
- **Processing Time**: 1-3 seconds per case
- **Memory Usage**: Minimal (no ML models loaded)
- **Scalability**: Can process multiple cases sequentially

Future performance (with LLM):
- **Processing Time**: 10-30 seconds per case (depending on hardware)
- **Memory Usage**: ~4-8 GB (for 7B parameter models)
- **Scalability**: Consider async processing for multiple cases

## Troubleshooting

### Issue: Import Error

```python
# Error: ModuleNotFoundError: No module named 'ai_layer'
```

**Solution**: Make sure you're in the correct directory:
```bash
cd "E:\web dev\SVNIT"
python -c "from ai_layer import run_ai_pipeline; print('Success!')"
```

### Issue: Validation Failed

```python
# Error: Validation failed for case
```

**Solution**: Check your forensic data structure:
```python
from ai_layer.ingestion_api import ForensicArtefactIngestionAPI

api = ForensicArtefactIngestionAPI()
is_valid, errors = api.validate_forensic_data(forensic_data)

if not is_valid:
    print("Validation errors:", errors)
```

### Issue: Empty Report

```python
# AI report has no interpretations
```

**Solution**: Ensure your forensic data has events and findings:
```python
print(f"Events: {len(forensic_data['timeline']['events'])}")
print(f"Findings: {sum(len(v) for v in forensic_data['findings'].values())}")
```

## Next Steps

1. ✅ Run `demo_integration.py` to see the system in action
2. ✅ Review `flask_integration_example.py` for Flask patterns
3. ✅ Test with your actual forensic data
4. ✅ Integrate into your existing `app.py`
5. ⏳ Wait for multilingual module from teammate
6. ⏳ Future: Upgrade to LLM-based interpretation

## Support

For questions:
1. Check `README.md` for architecture overview
2. Review `design.md` for component details
3. See `requirements.md` for specifications
4. Examine code comments and docstrings

## License

Part of the Forensi-Guard project.
