# Demo Case User Guide

## What is the Demo Case?

The Demo Case is a pre-loaded forensic analysis scenario that demonstrates the full capabilities of Forensi-Guard without requiring you to extract data from a real device. It showcases a **high-risk surveillance detection** scenario.

## How to Use the Demo Case

### Step 1: Start the Application
```bash
python app.py
```
Then open your browser to: `http://127.0.0.1:5000`

### Step 2: Select the Demo Case

On the homepage, you'll see a dropdown menu labeled **"Select Investigation Case"**. The first option will be:

```
🔴 Demo Case - Suspicious Surveillance Activity (High Risk)
```

This is your demo case - it's marked with a red circle (🔴) to indicate it's a high-risk scenario.

### Step 3: Choose Your Language

Select your preferred language from the dropdown:
- **English** - Full English report
- **हिन्दी (Hindi)** - Complete Hindi translation
- **ગુજરાતી (Gujarati)** - Complete Gujarati translation

All forensic evidence (timestamps, app names, numbers) remains unchanged across languages.

### Step 4: Run Analysis

Click the **"Run Analysis"** button. The analysis completes instantly (< 0.1 seconds).

### Step 5: View Results

You'll be redirected to the results page showing:

## What You'll See in the Demo Report

### 1. Case Information
```
Investigation Report
Case: 🔴 Demo Case - Suspicious Surveillance Activity (High Risk)
[DEMO CASE badge]

ℹ️ Note: This is a demonstration case showcasing high-risk surveillance 
detection capabilities. No real user data is involved.

Language: English / हिन्दी / ગુજરાતી
```

### 2. Threat Summary
```
⚠️ Threat Summary
High-risk threat: Suspicious location tracking activity detected 
with privacy implications.
```

### 3. Risk Assessment
```
🟥 Risk Assessment

┌─────────────┐
│    HIGH     │  ← Large, red box
└─────────────┘

Risk Score: 76.0/100
Confidence: 75%
Reasoning: Multiple high-severity findings detected including malware 
indicators and suspicious behaviour patterns. The presence of stalkerware 
signatures and excessive permission abuse indicates significant privacy 
and security risks.
```

### 4. Key Findings (5 findings)
```
🔍 Key Findings

1. The app com.tracker.stealth has permission to access your precise 
   GPS location. This allows the app to track your exact coordinates.
   (Confidence: 80%)

2. The app com.tracker.stealth has permission to access your precise 
   GPS location. This allows the app to track your exact coordinates.
   (Confidence: 80%)

3. SMS from sender +91XXXXXXXXXX at 2026-02-10T18:20:00 contains 
   authentication-related content: Your verification code is 456789
   (Confidence: 70%)

4. Incoming call from +91XXXXXXXXXX at 2026-02-11T02:15:00 lasted 
   120 seconds
   (Confidence: 60%)

5. Photo IMG_20260211_154500.jpg taken at 2026-02-11T15:45:00 contains 
   GPS coordinates: 23.0225, 72.5714
   (Confidence: 90%)

Total artefacts analyzed: 9
```

### 5. Timeline Narrative
```
🕒 Timeline Narrative

The forensic analysis examined device activity from 2026-02-10T14:30:00 
to 2026-02-11T15:45:00. During this period, several significant events 
were identified. The app com.tracker.stealth was installed at 
2026-02-10T14:30:00, followed by location permission being granted at 
2026-02-10T14:35:00. An SMS with verification code was received at 
2026-02-10T18:20:00. An incoming call from unknown number occurred at 
2026-02-11T02:15:00. A photo with GPS metadata was captured at 
2026-02-11T15:45:00.

Detected Patterns:
• App installation followed by immediate permission requests
• SMS activity involving verification codes
• Late-night communication activity (02:15:00)
```

### 6. Safety Recommendations (5 recommendations)
```
🛡️ Safety Recommendations

Priority: High

1. [Immediate Action] Review and disable suspicious applications immediately
   Priority: High
   Reasoning: Immediate action required to prevent further privacy violations
   Steps:
   • Open device Settings
   • Navigate to Apps or Application Manager
   • Review recently installed apps
   • Disable or uninstall suspicious applications
   • Revoke unnecessary permissions

2. [Professional Help] Contact local cyber harassment support services 
   or law enforcement
   Priority: High
   Reasoning: Professional assistance recommended for serious threats
   Steps:
   • Document all suspicious activity
   • Contact local cybercrime cell
   • Seek legal advice if needed
   • Report to relevant authorities

3. [Evidence Preservation] Preserve device evidence for potential 
   legal proceedings
   Priority: Medium
   Reasoning: Evidence preservation important for legal action
   Steps:
   • Do not delete suspicious apps yet
   • Take screenshots of suspicious activity
   • Backup device data securely
   • Maintain chain of custody

4. [Security Measures] Review and revoke excessive app permissions
   Priority: Medium
   Reasoning: Limiting app permissions reduces privacy risks
   Steps:
   • Review all app permissions
   • Revoke unnecessary location access
   • Disable background data for suspicious apps
   • Enable permission monitoring

5. [Monitoring] Monitor device for continued suspicious activity
   Priority: Low
   Reasoning: Ongoing monitoring helps detect new threats
   Steps:
   • Check battery usage regularly
   • Monitor data usage patterns
   • Review app activity logs
   • Install security monitoring tools

Disclaimer: These recommendations are AI-generated suggestions based on 
forensic analysis. For serious threats, always consult with cybersecurity 
professionals and law enforcement authorities.
```

## Demo Case Scenario Details

### The Story
This demo case simulates a real-world cyber harassment scenario where:

1. **A tracking app was installed** on the device (com.tracker.stealth)
2. **The app requested excessive permissions** (GPS, contacts, SMS, camera)
3. **Background tracking was enabled** (every 3 minutes for 72 hours)
4. **The app icon was hidden** from the launcher
5. **Late-night suspicious activity** was detected
6. **Malware signatures matched** known stalkerware patterns

### Why This Matters
This scenario demonstrates:
- **Stalkerware detection** - Identifying hidden surveillance apps
- **Permission abuse** - Recognizing excessive permission requests
- **Behavioral analysis** - Detecting suspicious activity patterns
- **Timeline reconstruction** - Understanding the sequence of events
- **Risk assessment** - Quantifying the threat level
- **Safety guidance** - Providing actionable recommendations

## Key Features Demonstrated

### 1. Evidence Integrity
All forensic evidence is preserved exactly:
- ✅ Timestamps: `2026-02-10T14:30:00`
- ✅ Package names: `com.tracker.stealth`
- ✅ Phone numbers: `+91XXXXXXXXXX`
- ✅ GPS coordinates: `23.0225, 72.5714`
- ✅ File hashes: `a1b2c3d4e5f6...`

### 2. Multilingual Support
The same analysis in three languages:
- **English**: Full technical detail
- **Hindi**: Complete translation with preserved evidence
- **Gujarati**: Complete translation with preserved evidence

### 3. Explainable AI
Every finding includes:
- Plain-language explanation
- Confidence score
- Reasoning
- Context

### 4. Risk Scoring
Transparent risk calculation:
- **Risk Level**: High/Medium/Low
- **Risk Score**: 0-100 numerical score
- **Confidence**: AI confidence in assessment
- **Reasoning**: Why this risk level was assigned

### 5. Timeline Analysis
Chronological narrative showing:
- Event sequence
- Pattern detection
- Time gaps
- Key events

### 6. Safety Recommendations
Prioritized, actionable guidance:
- Category (Immediate Action, Professional Help, etc.)
- Priority level (High, Medium, Low)
- Reasoning
- Step-by-step instructions

## Comparison: Demo vs Real Cases

| Feature | Demo Case | Real Cases |
|---------|-----------|------------|
| Data Source | Pre-loaded JSON | Forensic extraction |
| Processing Time | Instant (<0.1s) | ~0.5-2s |
| Risk Level | Always HIGH | Varies by data |
| Findings | 5 key findings | Varies by data |
| Purpose | Demonstration | Actual investigation |
| Data Privacy | No real data | User's device data |
| Editability | Read-only | Read-only |

## When to Use the Demo Case

### ✅ Good Use Cases
- **First-time users** exploring the system
- **Judges/evaluators** reviewing capabilities
- **Presentations** and demonstrations
- **Testing** the interface and features
- **Learning** how the system works
- **Language testing** across Hindi/Gujarati

### ❌ Not Suitable For
- **Actual investigations** (use real forensic data)
- **Legal proceedings** (requires authentic evidence)
- **Personal device analysis** (extract your own data)
- **Training on real scenarios** (use actual cases)

## Tips for Demonstrating

### For Presentations
1. Start with the demo case to show capabilities
2. Explain each section as you scroll through results
3. Switch languages to show multilingual support
4. Highlight the risk score and key findings
5. Show the safety recommendations

### For Judges/Evaluators
1. Run the demo case first for quick overview
2. Then run a real case (case_001 or case_002) for comparison
3. Show the extraction guide for completeness
4. Demonstrate language switching
5. Explain the AI interpretation process

### For Users
1. Try the demo case first to understand the interface
2. Read through all sections carefully
3. Note the confidence scores
4. Review the safety recommendations
5. Then extract your own device data for real analysis

## Frequently Asked Questions

### Q: Is the demo case based on real data?
**A**: No, it's a synthetic scenario created for demonstration purposes. However, it's based on real-world stalkerware patterns and forensic indicators.

### Q: Can I modify the demo case?
**A**: The demo case is read-only and cannot be edited through the UI. Developers can modify `demo_case.json` if needed.

### Q: Why does the demo case always show HIGH risk?
**A**: The demo case is designed to showcase the system's ability to detect serious threats. It includes multiple high-severity indicators (stalkerware, hidden icon, excessive permissions, background tracking).

### Q: Does the demo case work in all languages?
**A**: Yes! The demo case works perfectly in English, Hindi, and Gujarati. All forensic evidence is preserved across translations.

### Q: How is the demo case different from real cases?
**A**: The demo case loads instantly and always produces the same results. Real cases require forensic data extraction and analysis varies based on actual device content.

### Q: Can I use the demo case for training?
**A**: Yes! The demo case is excellent for training users on how to interpret forensic reports and understand risk assessments.

## Technical Details

### Data Structure
The demo case uses the same data format as real forensic cases:
```json
{
  "case_id": "demo_case_001",
  "metadata": { ... },
  "timeline": { "events": [...] },
  "findings": {
    "malware_indicators": [...],
    "suspicious_behaviour": [...],
    "permission_abuse": [...]
  },
  "hashes": { ... }
}
```

### Processing Pipeline
The demo case goes through the same 6-step AI pipeline:
1. **Ingestion** - Validate and structure data
2. **Interpretation** - Generate plain-language explanations
3. **Risk Assessment** - Calculate risk score
4. **Timeline Narrative** - Create chronological story
5. **Safety Recommendations** - Generate actionable advice
6. **Formatting** - Structure final report

### Performance
- **Load Time**: Instant (file read)
- **Processing Time**: ~0.03 seconds
- **Translation Time**: ~0.02 seconds per language
- **Total Response**: <0.1 seconds

## Conclusion

The demo case is a powerful tool for:
- ✅ Understanding system capabilities
- ✅ Training new users
- ✅ Demonstrating to judges/evaluators
- ✅ Testing multilingual support
- ✅ Learning forensic interpretation
- ✅ Exploring the interface

**Ready to try it?** Run `python app.py` and select the 🔴 Demo Case!

---

*For questions or issues, refer to the main documentation or contact the development team.*
