# AI Intelligence Layer - Run Instructions

## ✅ System Status: VERIFIED & WORKING

All tests passed successfully. The AI Intelligence Layer is ready for integration.

---

## Quick Start

### 1. Run Tests (Verify System)

```bash
python ai_layer/test_pipeline.py
```

**Expected Output:**
- ✅ 5/5 tests passed
- Processing time: ~0.3 seconds total
- All components initialized successfully

**What This Tests:**
- Minimal forensic data handling
- Cases with findings
- Timeline narrative generation
- Safety recommendations
- Output format validation

---

### 2. Run Demo (See Full Pipeline)

```bash
python ai_layer/demo_integration.py
```

**Expected Output:**
- 🤖 AI processing started
- 6 processing steps completed
- Risk assessment: High (83.5/100)
- 12 plain-language interpretations
- Timeline narrative with 6 key events
- 5 safety recommendations
- Report saved to `ai_report_demo.json`

**What This Demonstrates:**
- Realistic forensic data simulation
- Complete AI pipeline execution
- Structured report generation
- Integration patterns

---

## Output Structure

The AI pipeline produces a structured JSON report:

```json
{
  "case_id": "case_demo_001",
  "language": "en",
  "generated_at": "2026-02-13T22:42:51.192362",
  "sections": {
    "executive_summary": {
      "risk_assessment": {
        "risk_level": "High",
        "risk_score": 83.5,
        "confidence": 77.5,
        "reasoning": "..."
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
      "narrative": "Chronological story of events...",
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
          "reasoning": "Why",
          "steps": [...]
        }
      ],
      "ai_generated": true
    }
  },
  "metadata": {
    "processing_time_seconds": 0.05,
    "confidence_average": 76.8
  }
}
```

---

## Integration with Your Forensic Backend

### Step 1: Import the Pipeline

```python
from ai_layer import run_ai_pipeline
```

### Step 2: Prepare Your Forensic Data

Your existing forensic engine should output:

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
        "events": [...]
    },
    "findings": {
        "suspicious_behaviour": [...],
        "malware_indicators": [...],
        "timestamp_anomalies": [...],
        "permission_abuse": [...]
    },
    "hashes": {
        "algorithm": "SHA-256",
        "files": [...]
    }
}
```

### Step 3: Process Through AI Layer

```python
# Run AI interpretation
ai_report = run_ai_pipeline(case_id, forensic_data, language="en")

# Access results
risk_level = ai_report["sections"]["executive_summary"]["risk_assessment"]["risk_level"]
narrative = ai_report["sections"]["timeline_narrative"]["narrative"]
recommendations = ai_report["sections"]["safety_recommendations"]["recommendations"]
```

---

## What's Working

### ✅ Evidence Interpretation
- **Location permissions** → "This app can track your location"
- **Contact permissions** → "This app can access your contacts"
- **SMS permissions** → "This app can read your messages"
- **Camera permissions** → "This app can access your camera"
- **Suspicious patterns** detected and explained

### ✅ Risk Scoring
- **Weighted algorithm**: Malware (40%), Behavior (35%), Anomalies (15%), Permissions (10%)
- **Risk levels**: Low (0-30), Medium (30-60), High (60-85), Critical (85-100)
- **Confidence scores**: Based on evidence quality and quantity
- **Reasoning**: Explains how score was calculated

### ✅ Timeline Narration
- **Chronological stories** from events
- **Key event identification** (high significance events highlighted)
- **Pattern detection** (rapid permissions, nighttime activity, etc.)
- **Temporal context** (first event to last event timeframe)

### ✅ Safety Recommendations
- **Immediate actions** for high-risk cases
- **Preventive measures** for ongoing security
- **Professional help** guidance when needed
- **Evidence preservation** instructions

### ✅ Complete Pipeline
- **Progress logging** with visual feedback
- **Error handling** with graceful degradation
- **Structured JSON** output
- **Processing time** tracking (~0.05 seconds per case)

---

## Performance

- **Processing Time**: 0.05-0.07 seconds per case
- **Memory Usage**: Minimal (no ML models loaded yet)
- **Scalability**: Can process cases sequentially
- **Error Rate**: 0% (all tests passed)

---

## Important Notes

### 1. Read-Only Operation
✅ The AI layer **NEVER** modifies forensic data
- All operations are read-only
- Original evidence is preserved
- AI outputs are separate from forensic data

### 2. AI-Generated Labels
✅ All AI outputs include `"ai_generated": true`
- Display this clearly in your UI
- Users must know content is AI-interpreted

### 3. Language Support
✅ Currently English only (`language="en"`)
- Hindi and Gujarati will be added by your teammate
- Translation integration points are marked with TODO

### 4. Mock AI Logic
✅ Current implementation uses rule-based logic
- **Evidence Interpretation**: Pattern matching
- **Risk Scoring**: Weighted algorithm
- **Timeline Narration**: Template-based
- **Recommendations**: Context-aware rules

Future versions will use:
- Local LLM (Llama 2 7B / Mistral 7B)
- Advanced NLG models
- ML-based confidence scoring

---

## Troubleshooting

### Issue: Import Error
```
ModuleNotFoundError: No module named 'ai_layer'
```

**Solution**: Run from the correct directory
```bash
cd "E:\web dev\SVNIT"
python ai_layer/test_pipeline.py
```

### Issue: No Output
```
Script runs but produces no output
```

**Solution**: Check that forensic_data has events and findings
```python
print(f"Events: {len(forensic_data['timeline']['events'])}")
print(f"Findings: {sum(len(v) for v in forensic_data['findings'].values())}")
```

### Issue: Low Risk Score
```
Risk score is always 0 or very low
```

**Solution**: Ensure findings have severity levels
```python
findings = {
    "malware_indicators": [
        {"type": "malware", "severity": "critical"}
    ]
}
```

---

## Next Steps

1. ✅ **Verified**: Run `python ai_layer/test_pipeline.py` → All tests passed
2. ✅ **Verified**: Run `python ai_layer/demo_integration.py` → Demo successful
3. 📝 **Next**: Review `flask_integration_example.py` for Flask patterns
4. 🔧 **Next**: Integrate into your existing `app.py`
5. ⏳ **Future**: Wait for multilingual module from teammate
6. ⏳ **Future**: Upgrade to LLM-based interpretation

---

## Support Files

- `README.md` - Architecture overview
- `INTEGRATION_GUIDE.md` - Detailed integration instructions
- `design.md` - Component specifications
- `requirements.md` - System requirements
- `flask_integration_example.py` - Flask integration patterns

---

## Success Criteria ✅

- [x] All tests pass (5/5)
- [x] Demo runs successfully
- [x] Output is structured and readable
- [x] Risk scoring works correctly
- [x] Timeline narratives are generated
- [x] Recommendations are contextual
- [x] Error handling is graceful
- [x] Processing time is fast (<0.1s per case)
- [x] System is integration-ready

---

**Status**: ✅ READY FOR INTEGRATION

The AI Intelligence Layer is fully functional and ready to be integrated with your existing Forensi-Guard forensic backend.
