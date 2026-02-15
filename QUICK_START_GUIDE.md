# Forensi-Guard - Quick Start Guide

## 🚀 Running the Application

```bash
python app.py
```

Then open: **http://127.0.0.1:5000**

---

## 📋 Using the System

### Step 1: Select a Case
Choose from available forensic cases:
- **case_001**: General Investigation (7 findings)
- **case_002**: Suspicious Activity (13 timestamp anomalies)
- **case_003**: Device Analysis (baseline case)

### Step 2: Select Language
Choose your preferred language:
- **English** (en)
- **Hindi** (hi)
- **Gujarati** (gu)

### Step 3: Run Analysis
Click "Run Analysis" button and wait 1-2 seconds

### Step 4: View Results
Results page shows:
- Case name and label
- Threat summary (one-line overview)
- Risk assessment (color-coded)
- Key findings
- Timeline narrative
- Safety recommendations

---

## 🧪 Running Tests

### Complete Workflow Test
```bash
python test_full_workflow.py
```
Tests all 3 cases with AI processing and translation

### Case Selection Test
```bash
python test_case_selection.py
```
Tests case detection and transformer

### Transformer Tests
```bash
python test_transformer.py      # Test case_001
python test_case_002.py          # Test case_002
```

### Flask Demo Test
```bash
python test_flask_demo.py
```
Tests Flask app and routes

### Multilingual Test
```bash
python test_multilingual_integration.py
```
Tests translation functionality

---

## 📁 Project Structure

```
.
├── app.py                              # Flask application (with transformer)
├── demo_case.json                      # Demo forensic data
├── templates/
│   ├── index.html                     # Home page (with case selector)
│   └── results.html                   # Results page (with case display)
├── static/
│   └── style.css                      # Styling
├── ai_layer/                          # AI Intelligence Layer
│   ├── ai_pipeline.py                 # Main pipeline
│   ├── formatter.py                   # Output formatting (with threat_summary)
│   ├── evidence_interpreter.py        # Evidence interpretation (enhanced)
│   ├── risk_engine.py                 # Risk assessment
│   ├── timeline_narrator.py           # Timeline narrative
│   ├── safety_advisor.py              # Safety recommendations
│   └── ingestion_api.py               # Data ingestion
├── language_layer/
│   └── translator.py                  # Translation (mock)
├── mobile-forensics-tool/
│   └── cases/                         # Forensic cases
│       ├── case_001/
│       ├── case_002/
│       └── case_003/
└── tests/
    ├── test_full_workflow.py          # Complete workflow test
    ├── test_case_selection.py         # Case selection test
    ├── test_transformer.py            # Transformer test
    ├── test_case_002.py               # Case 002 test
    ├── test_flask_demo.py             # Flask demo test
    └── test_multilingual_integration.py  # Translation test
```

---

## 🔧 Key Features

### 1. Dynamic Case Selection
- Auto-detects available cases
- Friendly case labels
- Case name displayed in results

### 2. Data Transformation
- Converts forensic report format to AI pipeline format
- Extracts findings from summary reports
- Categorizes findings intelligently
- Preserves evidence integrity

### 3. AI Intelligence Layer
- Interprets forensic evidence
- Assesses risk levels
- Generates timeline narratives
- Provides safety recommendations
- Creates threat summaries

### 4. Multilingual Support
- Translates to Hindi and Gujarati
- Preserves evidence data
- Maintains report structure
- Clean layer separation

### 5. Professional UI
- Clean, modern design
- Color-coded risk levels
- Responsive layout
- Loading animations
- Error handling

---

## 📊 System Flow

```
User Selects Case & Language
    ↓
Load forensic_report.json
    ↓
Transform to AI Format
    ↓
AI Pipeline Processing
    ↓
Generate Interpretations
    ↓
Assess Risk
    ↓
Create Narrative
    ↓
Generate Recommendations
    ↓
Translate (if needed)
    ↓
Display Results
```

---

## ⚙️ Configuration

### Adding New Cases
1. Place forensic report in `mobile-forensics-tool/cases/case_XXX/reports/forensic_report.json`
2. System auto-detects on next run
3. Add friendly label in `app.py` `CASE_LABELS` dictionary (optional)

### Adding Case Labels
Edit `app.py`:
```python
CASE_LABELS = {
    "case_001": "Case 001 - General Investigation",
    "case_002": "Case 002 - Suspicious Activity",
    "case_003": "Case 003 - Device Analysis",
    "case_004": "Your New Case Label"  # Add here
}
```

---

## 🐛 Troubleshooting

### Issue: No cases found
**Solution**: Check that `mobile-forensics-tool/cases` directory exists and contains valid case folders with `reports/forensic_report.json`

### Issue: Translation not working
**Solution**: Check that `language_layer/translator.py` exists and `TRANSLATION_AVAILABLE` is True in `app.py`

### Issue: AI pipeline fails
**Solution**: Check that forensic report has required structure. The transformer should handle most formats automatically.

### Issue: Port already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

---

## 📝 Important Notes

### Evidence Integrity
- System is READ-ONLY
- Never modifies forensic evidence
- All AI outputs marked as "AI-generated"
- Original forensic data preserved

### Limitations
- Summary reports have limited detailed data
- Risk scores may be lower without detailed events
- Timeline narrative minimal without event details
- Mock translation (not real translation service)

### Demo Purpose
- This is a PROTOTYPE for demonstration
- Not production-ready
- No authentication or user management
- Demo data only

---

## 🎯 Demo Tips

### For Video Recording:
1. Start with home page showing project intro
2. Demonstrate case selection dropdown
3. Show language selection
4. Click "Run Analysis" and show loading
5. Highlight key sections in results:
   - Threat summary
   - Risk assessment (color-coded)
   - Key findings
   - Recommendations
6. Go back and try different case/language combination

### For Live Demo:
1. Have app running before demo starts
2. Test all 3 cases beforehand
3. Test all 3 languages beforehand
4. Have backup plan if network issues
5. Explain architecture briefly
6. Emphasize evidence integrity preservation

---

## 📚 Documentation

- **COMPLETION_SUMMARY.md** - Complete task history
- **CASE_SELECTION_IMPLEMENTATION.md** - Technical details of transformer
- **TASK_6_COMPLETION_SUMMARY.md** - Task 6 detailed summary
- **FLASK_DEMO_README.md** - Flask demo documentation
- **MULTILINGUAL_INTEGRATION_SUMMARY.md** - Translation integration details
- **ai_layer/README.md** - AI layer documentation
- **ai_layer/INTEGRATION_GUIDE.md** - Integration guide
- **ai_layer/QUICK_REFERENCE.md** - AI layer quick reference

---

## ✅ Pre-Demo Checklist

- [ ] Run `python test_full_workflow.py` - all tests pass
- [ ] Test case_001 in browser
- [ ] Test case_002 in browser
- [ ] Test case_003 in browser
- [ ] Test English language
- [ ] Test Hindi language
- [ ] Test Gujarati language
- [ ] Check UI displays correctly
- [ ] Check all sections render properly
- [ ] Prepare demo script
- [ ] Test screen recording setup

---

## 🎉 Ready for Demo!

Your Forensi-Guard system is fully functional and ready for demonstration.

**Key Selling Points:**
- ✅ AI-assisted forensic interpretation
- ✅ Multiple case support
- ✅ Multilingual accessibility
- ✅ Evidence integrity preservation
- ✅ Clear, actionable insights
- ✅ Professional UI
- ✅ Comprehensive testing

**Good luck with your hackathon! 🚀**
