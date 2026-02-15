"""
AI Intelligence Layer for Forensi-Guard

This module provides assistive interpretation of forensic artefacts
without modifying original evidence. It acts as middleware between
the forensic engine and community interface.

Components:
- ingestion_api: Receives forensic data from existing engine
- evidence_interpreter: Converts technical artefacts to plain language
- risk_engine: Generates contextual risk assessments
- timeline_narrator: Creates narrative summaries from timelines
- safety_advisor: Provides advisory-only recommendations
- formatter: Formats AI outputs for delivery
- ai_pipeline: Main orchestration pipeline
"""

__version__ = "0.1.0"
__author__ = "Forensi-Guard Team"

from .ai_pipeline import run_ai_pipeline, process_case

__all__ = ["run_ai_pipeline", "process_case"]
