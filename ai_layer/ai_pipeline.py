"""
AI Intelligence Layer Pipeline

Main orchestration pipeline that coordinates all AI components.
Acts as middleware between the forensic engine and community interface.
"""

import logging
from typing import Dict, List
from datetime import datetime

# Use absolute imports when running as script, relative when imported as module
try:
    from .ingestion_api import ForensicArtefactIngestionAPI
    from .evidence_interpreter import AIEvidenceInterpreter
    from .risk_engine import AIRiskScoringEngine
    from .timeline_narrator import AITimelineNarrator
    from .safety_advisor import AISafetyAdvisor
    from .formatter import OutputFormattingAPI
except ImportError:
    from ingestion_api import ForensicArtefactIngestionAPI
    from evidence_interpreter import AIEvidenceInterpreter
    from risk_engine import AIRiskScoringEngine
    from timeline_narrator import AITimelineNarrator
    from safety_advisor import AISafetyAdvisor
    from formatter import OutputFormattingAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIPipeline:
    """
    Main AI Intelligence Layer pipeline.
    
    Orchestrates all AI components to process forensic data and generate
    interpretations, risk assessments, narratives, and recommendations.
    """
    
    def __init__(self):
        """Initialize all AI components."""
        logger.info("Initializing AI Intelligence Layer Pipeline")
        
        try:
            self.ingestion_api = ForensicArtefactIngestionAPI()
            self.evidence_interpreter = AIEvidenceInterpreter()
            self.risk_engine = AIRiskScoringEngine()
            self.timeline_narrator = AITimelineNarrator()
            self.safety_advisor = AISafetyAdvisor()
            self.formatter = OutputFormattingAPI()
            
            logger.info("AI Pipeline initialized successfully")
            
        except Exception as e:
            logger.exception("Error initializing AI Pipeline")
            raise
    
    def process_case(self, case_id: str, forensic_data: Dict, 
                    language: str = "en") -> Dict:
        """
        Process a complete forensic case through the AI pipeline.
        
        This is the main entry point for AI processing. It coordinates
        all components to generate a complete AI-interpreted report.
        
        Args:
            case_id: Unique case identifier
            forensic_data: Forensic data from existing engine containing:
                - metadata: Case metadata
                - timeline: Timeline events
                - findings: Analysis findings
                - hashes: SHA-256 hashes
            language: Target language for output (en, hi, gu)
        
        Returns:
            dict: Complete AI-interpreted report
            
        Example:
            >>> pipeline = AIPipeline()
            >>> result = pipeline.process_case("case_001", forensic_data)
            >>> print(result["sections"]["executive_summary"])
        """
        print("\n" + "="*70)
        print("🤖 AI INTELLIGENCE LAYER - PROCESSING STARTED")
        print("="*70)
        logger.info(f"Processing case: {case_id}")
        start_time = datetime.now()
        
        try:
            # Step 1: Ingest and validate forensic data
            print("\n[Step 1/6] 📥 Ingesting forensic data...")
            logger.info("Step 1: Ingesting forensic data")
            ingestion_result = self.ingestion_api.ingest_case_data(case_id, forensic_data)
            
            if ingestion_result.get("status") != "success":
                logger.error(f"Ingestion failed: {ingestion_result}")
                print("❌ Ingestion failed!")
                return self._create_error_response(case_id, "Ingestion failed", ingestion_result)
            
            print(f"✅ Validated {ingestion_result.get('artefact_count', 0)} artefacts")
            
            # Step 2: Interpret evidence artefacts
            print("\n[Step 2/6] 🔍 Interpreting evidence artefacts...")
            logger.info("Step 2: Interpreting evidence artefacts")
            interpretations = self._interpret_evidence(forensic_data)
            print(f"✅ Generated {len(interpretations)} plain-language interpretations")
            
            # Step 3: Generate risk assessment
            print("\n[Step 3/6] ⚠️  Generating risk assessment...")
            logger.info("Step 3: Generating risk assessment")
            risk_assessment = self._assess_risk(forensic_data)
            risk_level = risk_assessment.get("risk_level", "Unknown")
            risk_score = risk_assessment.get("risk_score", 0)
            print(f"✅ Risk Score: {risk_score:.1f}/100 (Level: {risk_level})")
            
            # Step 4: Generate timeline narrative
            print("\n[Step 4/6] 📖 Generating timeline narrative...")
            logger.info("Step 4: Generating timeline narrative")
            timeline_narrative = self._generate_timeline_narrative(forensic_data)
            event_count = timeline_narrative.get("event_count", 0)
            print(f"✅ Created narrative from {event_count} timeline events")
            
            # Step 5: Generate safety recommendations
            print("\n[Step 5/6] 🛡️  Generating safety recommendations...")
            logger.info("Step 5: Generating safety recommendations")
            recommendations = self._generate_recommendations(risk_assessment, forensic_data)
            rec_count = len(recommendations.get("recommendations", []))
            rec_priority = recommendations.get("priority", "Medium")
            print(f"✅ Generated {rec_count} recommendations (Priority: {rec_priority})")
            
            # Step 6: Format complete report
            print("\n[Step 6/6] 📄 Formatting complete report...")
            logger.info("Step 6: Formatting complete report")
            ai_outputs = {
                "interpretations": interpretations,
                "risk_assessment": risk_assessment,
                "timeline_narrative": timeline_narrative,
                "recommendations": recommendations
            }
            
            report = self.formatter.format_case_report(case_id, ai_outputs, language)
            
            # Add processing metadata
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            report["metadata"]["processing_time_seconds"] = processing_time
            
            print(f"✅ Report formatted successfully")
            
            print("\n" + "="*70)
            print(f"✅ AI PROCESSING COMPLETE in {processing_time:.2f} seconds")
            print("="*70 + "\n")
            
            logger.info(f"Case processing complete in {processing_time:.2f} seconds")
            return report
            
        except Exception as e:
            logger.exception(f"Error processing case {case_id}")
            print(f"\n❌ ERROR: {str(e)}")
            print("="*70 + "\n")
            return self._create_error_response(case_id, "Processing failed", str(e))
    
    def _interpret_evidence(self, forensic_data: Dict) -> List[Dict]:
        """
        Interpret all evidence artefacts.
        
        Args:
            forensic_data: Forensic data from engine
            
        Returns:
            list: Interpretation results
        """
        interpretations = []
        
        # Interpret timeline events
        timeline = forensic_data.get("timeline", {})
        events = timeline.get("events", [])
        
        for event in events:
            source = event.get("source", "unknown")
            interpretation = self.evidence_interpreter.interpret_artefact(event, source)
            interpretations.append(interpretation)
        
        # Interpret findings
        findings = forensic_data.get("findings", {})
        for finding_type, finding_list in findings.items():
            if isinstance(finding_list, list):
                for finding in finding_list:
                    interpretation = self.evidence_interpreter.interpret_artefact(
                        finding, "finding"
                    )
                    interpretations.append(interpretation)
        
        logger.info(f"Generated {len(interpretations)} interpretations")
        return interpretations
    
    def _assess_risk(self, forensic_data: Dict) -> Dict:
        """
        Generate risk assessment.
        
        Args:
            forensic_data: Forensic data from engine
            
        Returns:
            dict: Risk assessment result
        """
        # Extract findings for risk scoring
        findings = []
        findings_data = forensic_data.get("findings", {})
        
        for finding_type, finding_list in findings_data.items():
            if isinstance(finding_list, list):
                for finding in finding_list:
                    findings.append({
                        "type": finding_type,
                        "data": finding,
                        "severity": finding.get("severity", "medium")
                    })
        
        # Extract context
        context = forensic_data.get("metadata", {})
        
        # Generate risk assessment
        risk_assessment = self.risk_engine.score_risk(findings, context)
        
        return risk_assessment
    
    def _generate_timeline_narrative(self, forensic_data: Dict) -> Dict:
        """
        Generate timeline narrative.
        
        Args:
            forensic_data: Forensic data from engine
            
        Returns:
            dict: Timeline narrative result
        """
        timeline = forensic_data.get("timeline", {})
        events = timeline.get("events", [])
        
        narrative = self.timeline_narrator.generate_narrative(events)
        
        return narrative
    
    def _generate_recommendations(self, risk_assessment: Dict, 
                                 forensic_data: Dict) -> Dict:
        """
        Generate safety recommendations.
        
        Args:
            risk_assessment: Risk assessment result
            forensic_data: Forensic data from engine
            
        Returns:
            dict: Safety recommendations
        """
        # Extract findings
        findings = []
        findings_data = forensic_data.get("findings", {})
        
        for finding_type, finding_list in findings_data.items():
            if isinstance(finding_list, list):
                findings.extend(finding_list)
        
        recommendations = self.safety_advisor.generate_recommendations(
            risk_assessment, findings
        )
        
        return recommendations
    
    def _create_error_response(self, case_id: str, error_type: str, 
                               error_details: any) -> Dict:
        """
        Create error response for failed processing.
        
        Args:
            case_id: Case identifier
            error_type: Type of error
            error_details: Error details
            
        Returns:
            dict: Error response
        """
        return {
            "case_id": case_id,
            "status": "error",
            "error_type": error_type,
            "error_details": str(error_details),
            "generated_at": datetime.now().isoformat(),
            "sections": {},
            "metadata": {
                "error": True
            }
        }


# Convenience functions for external integration

def run_ai_pipeline(case_id: str, forensic_data: Dict, 
                   language: str = "en") -> Dict:
    """
    Run the AI pipeline on forensic data.
    
    This is the main entry point for integrating with the existing
    forensic engine. Call this function with forensic data to get
    AI-interpreted results.
    
    Args:
        case_id: Unique case identifier
        forensic_data: Forensic data from existing engine
        language: Target language (en, hi, gu)
    
    Returns:
        dict: Complete AI-interpreted report
        
    Example:
        >>> from ai_layer import run_ai_pipeline
        >>> result = run_ai_pipeline("case_001", forensic_data)
        >>> print(result["sections"]["executive_summary"]["risk_assessment"])
    """
    pipeline = AIPipeline()
    return pipeline.process_case(case_id, forensic_data, language)


def process_case(case_id: str, forensic_data: Dict, 
                language: str = "en") -> Dict:
    """
    Alias for run_ai_pipeline for convenience.
    
    Args:
        case_id: Unique case identifier
        forensic_data: Forensic data from existing engine
        language: Target language (en, hi, gu)
    
    Returns:
        dict: Complete AI-interpreted report
    """
    return run_ai_pipeline(case_id, forensic_data, language)


# Example usage and integration guide
if __name__ == "__main__":
    """
    Example usage of the AI Intelligence Layer.
    
    This demonstrates how to integrate the AI layer with the existing
    forensic engine.
    """
    
    # Example forensic data structure (from existing engine)
    example_forensic_data = {
        "case_id": "case_001",
        "metadata": {
            "case_name": "Example Investigation",
            "investigator": "Officer Name",
            "device_type": "Android Device",
            "acquisition_method": "Logical (ADB)",
            "created_at": "2024-01-15T10:30:00Z"
        },
        "timeline": {
            "events": [
                {
                    "timestamp": "2024-01-10T14:23:00Z",
                    "source": "app",
                    "details": "Suspicious app installed",
                    "metadata": {}
                }
            ]
        },
        "findings": {
            "suspicious_behaviour": [
                {
                    "type": "suspicious_behaviour",
                    "description": "Unusual background activity",
                    "severity": "medium"
                }
            ],
            "malware_indicators": [],
            "timestamp_anomalies": []
        },
        "hashes": {
            "algorithm": "SHA-256",
            "files": []
        }
    }
    
    # Process the case through AI pipeline
    logger.info("Running example AI pipeline processing")
    result = run_ai_pipeline("case_001", example_forensic_data, language="en")
    
    # Display results
    print("\n" + "="*60)
    print("AI INTELLIGENCE LAYER - EXAMPLE OUTPUT")
    print("="*60)
    print(f"\nCase ID: {result.get('case_id')}")
    print(f"Language: {result.get('language')}")
    print(f"Generated: {result.get('generated_at')}")
    
    if "sections" in result:
        exec_summary = result["sections"].get("executive_summary", {})
        risk = exec_summary.get("risk_assessment", {})
        print(f"\nRisk Level: {risk.get('risk_level')}")
        print(f"Risk Score: {risk.get('risk_score')}")
        print(f"Confidence: {risk.get('confidence')}")
    
    print("\n" + "="*60)
    print("Integration successful! AI layer is ready for use.")
    print("="*60 + "\n")
