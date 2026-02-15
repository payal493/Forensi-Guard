# Design Document: AI Intelligence Layer

## Overview

The AI Intelligence Layer is a modular interpretation system that sits between the existing Forensi-Guard forensic engine and the community interface. It transforms technical forensic outputs into accessible, multilingual narratives while maintaining strict evidence integrity and explainability. The AI Intelligence Layer functions as an interpretation middleware and never performs evidence acquisition, modification, or forensic analysis, ensuring strict separation between AI reasoning and evidentiary processing.

### Design Principles

1. **Privacy-First Architecture**: Local processing prioritized, external API calls minimized and anonymized
2. **Read-Only Evidence Access**: All forensic artefacts accessed in read-only mode
3. **Explainable AI**: Every interpretation includes reasoning, confidence levels, and alternative explanations
4. **Modular Integration**: Clean API boundaries with existing forensic engine
5. **Graceful Degradation**: System remains functional even when AI components fail
6. **Human-Centric Safety Design**: AI outputs prioritize clarity for non-technical users while preserving forensic accuracy

### Technology Stack

- **Backend Framework**: Python Flask (matching existing forensic engine)
- **AI/ML Libraries**: 
  - Hugging Face Transformers (local LLM inference)
  - spaCy (NLP processing)
  - sentence-transformers (semantic analysis)
- **Translation**: 
  - IndicTrans2 (English ↔ Hindi/Gujarati)
  - Fallback: Google Translate API (with anonymization)
- **Data Format**: JSON for all inter-component communication
- **Logging**: Python logging module with forensic audit trail

## Architecture

### System Context

```
┌─────────────────────────────────────────────────────────────┐
│                    Forensi-Guard Platform                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐      ┌──────────────────────┐         │
│  │ Forensic Engine  │──────│ AI Intelligence      │         │
│  │ (EXISTING)       │ JSON │ Layer (NEW)          │         │
│  │                  │      │                      │         │
│  │ • ADB Acquisition│      │ • Evidence Interpreter│        │
│  │ • SHA-256 Hashing│      │ • Risk Scoring       │         │
│  │ • Timeline Recon │      │ • Timeline Narrator  │         │
│  │ • Rule-based     │      │ • Multilingual       │         │
│  │   Anomaly        │      │ • Safety Advisor     │         │
│  └──────────────────┘      └──────────────────────┘         │
│                                      │                        │
│                                      │ JSON                   │
│                                      ▼                        │
│                          ┌──────────────────────┐            │
│                          │ Community Interface  │            │
│                          │ (Future)             │            │
│                          └──────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              AI Intelligence Layer Components                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Forensic Artefact Ingestion API            │   │
│  │  (Receives JSON from Forensic Engine)                │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Core Processing Pipeline                 │   │
│  │                                                        │   │
│  │  ┌─────────────────┐  ┌──────────────────┐          │   │
│  │  │ AI Evidence     │  │ AI Risk Scoring  │          │   │
│  │  │ Interpreter     │  │ Engine           │          │   │
│  │  └─────────────────┘  └──────────────────┘          │   │
│  │                                                        │   │
│  │  ┌─────────────────┐  ┌──────────────────┐          │   │
│  │  │ AI Timeline     │  │ AI Safety        │          │   │
│  │  │ Narrator        │  │ Advisor          │          │   │
│  │  └─────────────────┘  └──────────────────┘          │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Multilingual Accessibility Module             │   │
│  │  (English, Hindi, Gujarati)                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Output Formatting & Delivery API           │   │
│  │  (Provides JSON to Community Interface)              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Forensic Artefact Ingestion API

**Purpose**: Receive forensic data from the existing forensic engine

**Interface**:
```python
class ForensicArtefactIngestionAPI:
    def ingest_case_data(self, case_id: str, forensic_data: dict) -> dict:
        """
        Ingest forensic data for a specific case.
        
        Args:
            case_id: Unique case identifier
            forensic_data: Dictionary containing:
                - timeline: List of timeline events
                - findings: Analysis findings (behaviour, malware, anomalies)
                - hashes: SHA-256 hash manifest
                - metadata: Case metadata
        
        Returns:
            dict: Ingestion status and validation results
        """
        pass
    
    def validate_forensic_data(self, forensic_data: dict) -> tuple[bool, list[str]]:
        """
        Validate forensic data structure and integrity.
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        pass
```

**Input Format** (from existing forensic engine):
```json
{
  "case_id": "case_001",
  "metadata": {
    "case_name": "Investigation XYZ",
    "investigator": "Officer Name",
    "device_type": "Android Device",
    "acquisition_method": "Logical (ADB)",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "timeline": {
    "events": [
      {
        "timestamp": "2024-01-10T14:23:00Z",
        "source": "SMS",
        "details": "Message received from +91XXXXXXXXXX",
        "metadata": {}
      }
    ]
  },
  "findings": {
    "suspicious_behaviour": [],
    "malware_indicators": [],
    "timestamp_anomalies": []
  },
  "hashes": {
    "algorithm": "SHA-256",
    "files": []
  }
}
```

### 2. AI Evidence Interpreter

**Purpose**: Convert technical forensic artefacts into plain-language explanations

**Interface**:
```python
class AIEvidenceInterpreter:
    def interpret_artefact(self, artefact: dict, artefact_type: str) -> dict:
        """
        Generate plain-language explanation for a forensic artefact.
        
        Args:
            artefact: Forensic artefact data
            artefact_type: Type (sms, call, app, media, finding)
        
        Returns:
            dict: {
                "original": artefact,
                "interpretation": str,
                "confidence": float (0-100),
                "reasoning": str,
                "alternatives": list[dict],
                "ai_generated": True
            }
        """
        pass
    
    def batch_interpret(self, artefacts: list[dict]) -> list[dict]:
        """Interpret multiple artefacts efficiently."""
        pass
```

**Implementation Strategy**:
- Use local LLM (e.g., Llama 2 7B, Mistral 7B) for interpretation
- Prompt engineering with forensic context
- Confidence scoring based on model perplexity and semantic coherence
- Alternative explanations generated via beam search or temperature sampling

**Example Transformation**:
```
Input (Technical):
{
  "type": "app_permission",
  "app": "com.example.tracker",
  "permission": "ACCESS_FINE_LOCATION",
  "granted": true
}

Output (Plain Language):
{
  "interpretation": "An app called 'tracker' has permission to access your exact location using GPS. This means the app can track where you are at any time.",
  "confidence": 85.0,
  "reasoning": "The permission ACCESS_FINE_LOCATION is a standard Android permission that allows precise location tracking. The app name suggests tracking functionality.",
  "alternatives": [
    {
      "interpretation": "This app can see your location for navigation or location-based services.",
      "confidence": 75.0
    }
  ],
  "ai_generated": true
}
```

### 3. AI Risk Scoring Engine

**Purpose**: Generate contextual risk assessments with reasoning

**Interface**:
```python
class AIRiskScoringEngine:
    def score_risk(self, findings: list[dict], context: dict) -> dict:
        """
        Generate risk score for detected activities.
        
        Args:
            findings: List of analysis findings
            context: Case context (device type, user profile, etc.)
        
        Returns:
            dict: {
                "risk_score": float (0-100),
                "risk_level": str (Low/Medium/High/Critical),
                "confidence": float (0-100),
                "reasoning": str,
                "contributing_factors": list[dict],
                "ai_generated": True
            }
        """
        pass
    
    def explain_risk_factors(self, findings: list[dict]) -> list[dict]:
        """Explain how each finding contributes to risk score."""
        pass
```

**Risk Scoring Algorithm**:
1. **Base Score Calculation**: Weighted sum of finding severities
2. **Contextual Adjustment**: Adjust based on device type, user profile
3. **Confidence Calculation**: Based on evidence quality and quantity
4. **Factor Weighting**:
   - Malware indicators: 40%
   - Suspicious behaviour: 35%
   - Timestamp anomalies: 15%
   - Permission abuse: 10%

**Example Output**:
```json
{
  "risk_score": 72.5,
  "risk_level": "High",
  "confidence": 88.0,
  "reasoning": "Multiple indicators suggest potential stalkerware activity. The device has apps with excessive location and communication permissions, combined with suspicious background activity patterns.",
  "contributing_factors": [
    {
      "factor": "Location tracking app with hidden icon",
      "weight": 0.35,
      "severity": "High"
    },
    {
      "factor": "Unusual SMS forwarding behavior detected",
      "weight": 0.25,
      "severity": "Medium"
    }
  ],
  "ai_generated": true
}
```

### 4. AI Timeline Narrator

**Purpose**: Transform technical timelines into narrative summaries

**Interface**:
```python
class AITimelineNarrator:
    def generate_narrative(self, timeline_events: list[dict]) -> dict:
        """
        Generate narrative summary from timeline events.
        
        Args:
            timeline_events: List of timeline events
        
        Returns:
            dict: {
                "narrative": str,
                "key_events": list[dict],
                "patterns": list[str],
                "gaps": list[dict],
                "confidence": float (0-100),
                "ai_generated": True
            }
        """
        pass
    
    def identify_key_events(self, timeline_events: list[dict]) -> list[dict]:
        """Identify and highlight significant events."""
        pass
    
    def detect_patterns(self, timeline_events: list[dict]) -> list[str]:
        """Detect suspicious patterns in timeline."""
        pass
```

**Narrative Generation Strategy**:
1. **Event Clustering**: Group related events by time and type
2. **Pattern Detection**: Identify suspicious sequences (e.g., install → permission grant → data access)
3. **Key Event Extraction**: Highlight events with high forensic significance
4. **Gap Analysis**: Identify missing time periods or data
5. **Narrative Construction**: Generate chronological story using NLG

**Example Output**:
```json
{
  "narrative": "On January 10th at 2:23 PM, a suspicious app was installed on the device. Within minutes, this app requested and received permission to access location, contacts, and messages. Over the next three days, the app was active in the background during nighttime hours, suggesting covert monitoring activity.",
  "key_events": [
    {
      "timestamp": "2024-01-10T14:23:00Z",
      "description": "Suspicious app installation",
      "significance": "High"
    }
  ],
  "patterns": [
    "Rapid permission escalation after installation",
    "Nighttime background activity",
    "Location tracking during movement"
  ],
  "gaps": [
    {
      "start": "2024-01-11T00:00:00Z",
      "end": "2024-01-11T06:00:00Z",
      "reason": "No device activity recorded (device may have been off)"
    }
  ],
  "confidence": 82.0,
  "ai_generated": true
}
```

### 5. Multilingual Accessibility Module

**Purpose**: Provide translations in English, Hindi, and Gujarati

**Interface**:
```python
class MultilingualAccessibilityModule:
    def translate(self, text: str, target_language: str) -> dict:
        """
        Translate text to target language.
        
        Args:
            text: Source text (English)
            target_language: Target language code (en, hi, gu)
        
        Returns:
            dict: {
                "original": str,
                "translated": str,
                "language": str,
                "confidence": float (0-100),
                "ai_generated": True
            }
        """
        pass
    
    def translate_report(self, report: dict, target_language: str) -> dict:
        """Translate entire report structure."""
        pass
    
    def get_supported_languages(self) -> list[str]:
        """Return list of supported language codes."""
        pass
```

**Translation Strategy**:
1. **Primary**: IndicTrans2 (local, privacy-preserving)
   - Specialized for Indian languages
   - Runs locally without external API calls
2. **Fallback**: Google Translate API
   - Used only when IndicTrans2 fails
   - Data anonymized before transmission (remove names, numbers, locations)
3. **Technical Term Handling**: Maintain glossary of forensic terms with approved translations
4. **Cultural Adaptation**: Adjust phrasing for cultural context while maintaining accuracy

**Example Translation**:
```json
{
  "original": "An app called 'tracker' has permission to access your exact location using GPS.",
  "translated": "एक ऐप जिसे 'ट्रैकर' कहा जाता है, उसे GPS का उपयोग करके आपकी सटीक स्थिति तक पहुंचने की अनुमति है।",
  "language": "hi",
  "confidence": 92.0,
  "ai_generated": true
}
```

### 6. AI Safety Advisor

**Purpose**: Generate advisory-only safety recommendations

**Interface**:
```python
class AISafetyAdvisor:
    def generate_recommendations(self, risk_assessment: dict, findings: list[dict]) -> dict:
        """
        Generate safety recommendations based on findings.
        
        Args:
            risk_assessment: Risk scoring output
            findings: Analysis findings
        
        Returns:
            dict: {
                "recommendations": list[dict],
                "priority": str (Low/Medium/High/Urgent),
                "disclaimer": str,
                "ai_generated": True
            }
        """
        pass
    
    def prioritize_recommendations(self, recommendations: list[dict]) -> list[dict]:
        """Sort recommendations by urgency and impact."""
        pass
```

**Recommendation Categories**:
1. **Immediate Actions**: Steps to take right now (e.g., "Disable suspicious app")
2. **Preventive Measures**: Long-term safety steps (e.g., "Review app permissions regularly")
3. **Professional Help**: When to seek expert assistance
4. **Evidence Preservation**: How to maintain evidence integrity

**Example Output**:
```json
{
  "recommendations": [
    {
      "category": "Immediate Action",
      "priority": "High",
      "action": "Disable the app 'com.example.tracker' immediately",
      "reasoning": "This app has excessive permissions and shows suspicious background activity",
      "steps": [
        "Go to Settings > Apps",
        "Find 'tracker' app",
        "Tap 'Disable' or 'Uninstall'"
      ]
    },
    {
      "category": "Professional Help",
      "priority": "High",
      "action": "Contact local cyber harassment support services",
      "reasoning": "The evidence suggests potential stalkerware, which may require legal intervention"
    }
  ],
  "priority": "High",
  "disclaimer": "These recommendations are advisory only and generated by AI. For legal or safety concerns, please consult with law enforcement or professional support services.",
  "ai_generated": true
}
```

### 7. Output Formatting & Delivery API

**Purpose**: Format and deliver AI-generated content to community interface

**Interface**:
```python
class OutputFormattingAPI:
    def format_case_report(self, case_id: str, ai_outputs: dict, language: str = "en") -> dict:
        """
        Format complete case report with all AI interpretations.
        
        Args:
            case_id: Case identifier
            ai_outputs: All AI-generated content
            language: Target language code
        
        Returns:
            dict: Formatted report ready for UI consumption
        """
        pass
    
    def get_case_report(self, case_id: str, language: str = "en") -> dict:
        """Retrieve formatted case report."""
        pass
```

**Output Format**:
```json
{
  "case_id": "case_001",
  "language": "en",
  "generated_at": "2024-01-15T10:30:00Z",
  "sections": {
    "executive_summary": {
      "risk_assessment": {},
      "key_findings": [],
      "ai_generated": true
    },
    "evidence_interpretation": {
      "artefacts": [],
      "ai_generated": true
    },
    "timeline_narrative": {
      "narrative": "",
      "key_events": [],
      "ai_generated": true
    },
    "safety_recommendations": {
      "recommendations": [],
      "ai_generated": true
    }
  },
  "metadata": {
    "ai_models_used": ["llama-2-7b", "indicTrans2"],
    "processing_time_seconds": 12.5,
    "confidence_average": 85.0
  }
}
```

## Data Models

### ForensicArtefact
```python
@dataclass
class ForensicArtefact:
    artefact_id: str
    artefact_type: str  # sms, call, app, media, finding
    timestamp: datetime
    raw_data: dict
    sha256_hash: str  # Hash of raw_data for integrity
    case_id: str
```

### AIInterpretation
```python
@dataclass
class AIInterpretation:
    interpretation_id: str
    artefact_id: str
    interpretation_text: str
    confidence_score: float  # 0-100
    reasoning: str
    alternative_interpretations: list[dict]
    model_used: str
    generated_at: datetime
    ai_generated: bool = True
```

### RiskAssessment
```python
@dataclass
class RiskAssessment:
    assessment_id: str
    case_id: str
    risk_score: float  # 0-100
    risk_level: str  # Low, Medium, High, Critical
    confidence_score: float  # 0-100
    reasoning: str
    contributing_factors: list[dict]
    generated_at: datetime
    ai_generated: bool = True
```

### TimelineNarrative
```python
@dataclass
class TimelineNarrative:
    narrative_id: str
    case_id: str
    narrative_text: str
    key_events: list[dict]
    detected_patterns: list[str]
    timeline_gaps: list[dict]
    confidence_score: float  # 0-100
    generated_at: datetime
    ai_generated: bool = True
```

### SafetyRecommendation
```python
@dataclass
class SafetyRecommendation:
    recommendation_id: str
    case_id: str
    category: str  # Immediate, Preventive, Professional, Evidence
    priority: str  # Low, Medium, High, Urgent
    action: str
    reasoning: str
    steps: list[str]
    generated_at: datetime
    ai_generated: bool = True
```

### TranslatedContent
```python
@dataclass
class TranslatedContent:
    translation_id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence_score: float  # 0-100
    translation_method: str  # indicTrans2, google_translate
    generated_at: datetime
    ai_generated: bool = True
```

### ProcessingLog
```python
@dataclass
class ProcessingLog:
    log_id: str
    case_id: str
    component: str  # interpreter, risk_scorer, narrator, etc.
    operation: str
    status: str  # success, failure, partial
    error_message: str | None
    processing_time_seconds: float
    timestamp: datetime
```

