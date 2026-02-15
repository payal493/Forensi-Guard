# Forensi-Guard Flask Demo UI

## Quick Start Guide

This is a minimal Flask-based web interface for demonstrating the Forensi-Guard AI Intelligence Layer.

### Prerequisites

```bash
pip install flask
```

### Running the Demo

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to: `http://127.0.0.1:5000`

3. **Run the demo:**
   - Click "Run Demo Analysis" button
   - Wait for AI processing (takes ~1-2 seconds)
   - View the formatted results

### File Structure

```
.
├── app.py                  # Flask application
├── demo_case.json          # Demo forensic data
├── templates/
│   ├── index.html         # Home page
│   └── results.html       # Results display
├── static/
│   └── style.css          # Styling
└── ai_layer/              # AI Intelligence Layer modules
```

### Features Demonstrated

1. **Home Page:**
   - Project introduction
   - Feature overview
   - Demo analysis trigger

2. **Results Page:**
   - Threat Summary (one-line overview)
   - Risk Assessment (color-coded)
   - Key Findings (with confidence scores)
   - Timeline Narrative
   - Safety Recommendations
   - Processing Metadata

### Demo Case

The `demo_case.json` file contains a realistic cyber harassment investigation scenario with:
- Suspicious tracking app installation
- Location permission grants
- SMS with verification codes
- Call logs
- Media files with GPS metadata
- Malware indicators
- Permission abuse findings

### UI Design

- Clean, centered layout
- Card-based sections
- Color-coded risk levels:
  - 🔴 Red = High/Critical
  - 🟠 Orange = Medium
  - 🟢 Green = Low
- Responsive design
- Minimal dependencies (no heavy frameworks)

### Important Notes

⚠️ **This is a PROTOTYPE interface for demonstration purposes only.**

- Read-only system (never modifies forensic evidence)
- All AI outputs marked as "AI-generated"
- Evidence integrity preserved
- Suitable for screen recording and hackathon demos

### Troubleshooting

**Port already in use:**
```bash
# Change port in app.py:
app.run(debug=True, host='127.0.0.1', port=5001)
```

**Module not found:**
```bash
# Ensure ai_layer is in the same directory
# Or adjust sys.path in app.py
```

**Demo case not found:**
```bash
# Ensure demo_case.json is in the root directory
```

### For Video Recording

1. Start the server
2. Open browser in full screen
3. Click "Run Demo Analysis"
4. Show the results page with all sections
5. Highlight:
   - Threat summary
   - Risk score
   - Key findings
   - Recommendations

### Next Steps

To integrate with your full forensic backend:

1. Replace `demo_case.json` with real forensic output
2. Modify `/analyze` route to load from your backend
3. Add authentication if needed
4. Deploy to production server

---

**Built for:** Forensi-Guard Hackathon Prototype  
**Purpose:** AI-assisted mobile forensics demonstration  
**Status:** Demo-ready ✅
