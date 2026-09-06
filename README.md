# Forensi-Guard 🔍

An automated, multi-layered digital forensics intelligence pipeline designed to ingest, analyze, and report on mobile device artifacts. Forensi-Guard processes heterogeneous data (SMS, Call Logs, Media, App footprints) and applies a weighted risk-scoring engine to detect anomalies, permission abuse, and evidence tampering.

## 🚀 Key Features

*   **Modular Evidence Ingestion:** Parses raw mobile forensic tool outputs into standardized formats using JSON schema validation.
*   **Weighted Risk Scoring:** Utilizes a strategy-pattern engine to evaluate threats based on weighted factors: Malware (40%), Behavioral Anomalies (35%), Timestamp Inconsistencies (15%), and Permission Abuse (10%).
*   **Temporal Anomaly Detection:** Identifies logical sequence violations and evidence tampering through deterministic timestamp normalization.
*   **Enterprise Reporting:** Generates comprehensive, court-ready forensic reports (Executive Summaries, Timelines, Interpretations) available in multiple languages (English, Hindi, Gujarati).
*   **Evidence Integrity:** Enforces read-only constraints and cryptographic hash correlation to ensure data remains court-admissible.

## 🛠️ Architecture & Tech Stack

*   **Backend Framework:** Python, Flask (RESTful API)
*   **Design Patterns:** Strategy (Risk Weights), Adapter (Format Transformation), Factory (Case Discovery), Decorator (Report Enhancement)
*   **Data Processing:** JSON Schema, Batch-optimized interpretation

## ⚙️ Installation & Usage

*(Note: Add your specific `pip install -r requirements.txt` and `python app.py` commands here based on how you run the tool locally)*