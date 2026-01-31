# Mobile Forensics Investigation Tool

A secure, rule-based mobile forensics investigation tool for 24-hour hackathon development.

## Purpose

This tool processes extracted Android phone data from the NIST CFReDS forensic reference dataset to:
- Extract and normalize mobile evidence (SMS, calls, media, apps)
- Detect suspicious behaviour using rule-based analysis
- Identify malware indicators and temporal anomalies
- Reconstruct unified event timelines
- Generate court-ready forensic reports with SHA-256 integrity verification
- Display findings in a secure, read-only web viewer

## Architecture

```
Raw Evidence (extracted files)
        ↓
Extraction (logical reading only)
        ↓
Processed JSON Evidence
        ↓
Analysis (rule-based, explainable)
        ↓
Findings + Hashes
        ↓
Timeline Reconstruction
        ↓
Secure Read-only Web Viewer + Report
```

## Directory Structure

```
mobile-forensics-tool/
├── evidence/
│   ├── raw/          # Input forensic evidence (copied manually)
│   ├── processed/    # Extracted JSON evidence
│   └── hashes/       # SHA-256 hashes
├── extractor/        # Data extraction scripts
├── analysis/         # Analysis + hashing scripts
├── timeline/         # Timeline reconstruction
├── reports/          # Report generation
└── ui/               # Flask secure viewer
```

## Security Constraints

- **READ-ONLY**: Evidence in `evidence/raw` is never modified
- **HASHING**: All evidence files are SHA-256 hashed for integrity
- **RULE-BASED**: Analysis uses explainable rules, not ML models
- **SECURE UI**: Web interface is read-only (no POST operations)
- **LOCAL ONLY**: No cloud connectivity or external dependencies

## JSON Schema

All extractors output JSON in this exact format:

```json
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "source": "SMS | CALL | MEDIA | APP",
  "type": "incoming | outgoing | created | deleted | modified",
  "details": "human-readable description"
}
```

## Quick Start

1. **Place evidence**: Copy NIST CFReDS dataset files to `evidence/raw/`
2. **Extract data**: Run extractor scripts to generate JSON evidence
3. **Analyze**: Execute analysis scripts for behaviour, malware, and anomaly detection
4. **Build timeline**: Run timeline reconstruction
5. **Generate report**: Create comprehensive forensic report
6. **View results**: Start Flask web viewer at `http://localhost:5000`

## Usage

### Extraction Phase
```bash
cd extractor
python extract_sms.py
python extract_calls.py
python extract_media.py
python extract_apps.py
```

### Analysis Phase
```bash
cd analysis
python hash_generator.py
python behaviour_analysis.py
python malware_analysis.py
python anomaly_analysis.py
```

### Timeline & Reports
```bash
cd timeline
python timeline_builder.py

cd ../reports
python generate_report.py
```

### Web Viewer
```bash
cd ui
python app.py
# Access at http://localhost:5000
```

## Components

### Extractors (`extractor/`)
- `extract_sms.py`: SMS message extraction and normalization
- `extract_calls.py`: Call log extraction and metadata parsing
- `extract_media.py`: Media file metadata and timestamp extraction
- `extract_apps.py`: Application usage and installation data extraction

### Analysis (`analysis/`)
- `hash_generator.py`: SHA-256 hashing for evidence integrity
- `behaviour_analysis.py`: Suspicious behaviour pattern detection
- `malware_analysis.py`: Malware indicator identification
- `anomaly_analysis.py`: Temporal anomaly and inconsistency detection

### Timeline (`timeline/`)
- `timeline_builder.py`: Unified chronological event reconstruction

### Reports (`reports/`)
- `generate_report.py`: Comprehensive forensic report generation

### Web UI (`ui/`)
- `app.py`: Secure read-only Flask web viewer

## Forensic Workflow

1. **Evidence Intake**: Raw forensic data placed in `evidence/raw/`
2. **Hash Verification**: Generate SHA-256 hashes for chain of custody
3. **Data Extraction**: Convert raw evidence to standardized JSON
4. **Rule-Based Analysis**: Apply forensic heuristics and rules
5. **Timeline Reconstruction**: Merge events chronologically
6. **Report Generation**: Create court-ready documentation
7. **Secure Viewing**: Display results in read-only web interface

## Important Notes

- This tool processes **already extracted** forensic data
- No direct phone connection or data acquisition
- All analysis is rule-based and explainable
- Evidence integrity is maintained through cryptographic hashing
- Web interface is strictly read-only for security

## Development Status

**Current State**: Complete skeleton implementation ready for data integration

**Next Steps**:
1. Implement actual extraction logic for NIST CFReDS dataset format
2. Define specific forensic rules for behaviour analysis
3. Add malware signature databases
4. Enhance timeline visualization
5. Expand report formatting

## Requirements

- Python 3.7+
- Flask (for web UI)
- Standard library modules only (no external dependencies for core functionality)
