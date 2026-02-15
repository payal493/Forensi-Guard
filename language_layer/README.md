# Forensi-Guard Multilingual Safety Summary Generator

A Python module that converts forensic risk insights into simplified safety explanations in English, Hindi, and Gujarati for victim safety and accessibility.

## Features

- **Multilingual Support**: Generates safety messages in English, Hindi, and Gujarati
- **Victim-Centric**: Uses non-technical language focused on safety
- **Offline Operation**: Works with local translation mappings, no external APIs required
- **Modular Design**: Easy to integrate with Flask backends and forensic pipelines
- **Extensible**: Support for custom translations and new issue types

## Supported Issue Types

- `location_tracking` - Apps accessing location data
- `suspicious_permissions` - Apps with unusual permissions
- `background_tracking` - Apps monitoring background activity
- `stalkerware_indicators` - Signs of monitoring software

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from safety_generator import SafetySummaryGenerator

# Initialize the generator
generator = SafetySummaryGenerator()

# Generate safety summary
result = generator.generate_safety_summary(
    risk_level="HIGH",
    issue_type="location_tracking",
    reasoning="App accesses precise location in background",
    confidence=0.87
)

print(result)
# Output:
# {
#     "english": "Your location is being tracked frequently. This could put your safety at risk. Consider reviewing app permissions.",
#     "hindi": "आपका स्थान लगातार ट्रैक किया जा रहा है। यह आपकी सुरक्षा को खतरा में डाल सकता है। ऐप अनुमतियां जांचें।",
#     "gujarati": "તમારું સ્થાન વારંવાર ટ્રેક કરવામાં આવી રહ્યું છે. આ તમારી સુરક્ષા માટે જોખમી હોઈ શકે છે. એપ પરવાનગીઓ તપાસો.",
#     "label": "AI-Generated Safety Insight"
# }
```

### Flask Integration

Run the Flask API server:

```bash
python flask_integration.py
```

The API will be available at `http://localhost:5000` with the following endpoints:

- `POST /api/safety-summary` - Generate safety summary
- `GET /api/supported-issues` - Get supported issue types
- `GET /api/health` - Health check
- `POST /api/add-translation` - Add custom translation

Example API call:

```bash
curl -X POST http://localhost:5000/api/safety-summary \
  -H 'Content-Type: application/json' \
  -d '{
    "risk_level": "HIGH",
    "issue_type": "location_tracking",
    "reasoning": "App accesses precise location in background",
    "confidence": 0.87
  }'
```

## API Reference

### SafetySummaryGenerator

#### Methods

##### `generate_safety_summary(risk_level, issue_type, reasoning, confidence)`

Generate multilingual safety summary based on risk analysis.

**Parameters:**
- `risk_level` (str): HIGH, MEDIUM, or LOW
- `issue_type` (str): Type of security issue
- `reasoning` (str): Technical reasoning from forensic analysis
- `confidence` (float): Confidence score (0.0 to 1.0)

**Returns:**
```python
{
    "english": "Safety message in English",
    "hindi": "Safety message in Hindi",
    "gujarati": "Safety message in Gujarati",
    "label": "AI-Generated Safety Insight"
}
```

##### `get_supported_issue_types()`

Return list of supported issue types.

##### `add_custom_translation(issue_type, risk_level, translations_dict)`

Add custom translation for new issue types.

**Parameters:**
- `issue_type` (str): New issue type identifier
- `risk_level` (str): HIGH, MEDIUM, or LOW
- `translations_dict` (dict): Translations for each language

## Example Usage

See `example_usage.py` for comprehensive examples including:

- Different risk levels and issue types
- Custom translations
- Error handling

## Design Constraints

- **Offline Operation**: No external paid APIs required
- **Victim-Centric**: Non-technical language focused on safety
- **No Legal Conclusions**: Focus on technical safety insights only
- **Modular**: Easy integration with existing forensic pipelines
- **Clear Interfaces**: Simple function signatures for easy integration

## File Structure

```
forensi-guard-multilingual-safety/
├── safety_generator.py      # Main module
├── example_usage.py         # Usage examples
├── flask_integration.py     # Flask API server
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## License

This module is part of the Forensi-Guard system for victim safety and mobile forensics interpretation.
