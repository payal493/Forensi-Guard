"""
Output Formatting & Delivery API

Formats AI-generated content for delivery to the community interface.
Structures all AI outputs into a consistent, consumable format.
"""

import logging
from typing import Dict, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class OutputFormattingAPI:
    """
    Formats and delivers AI-generated content to the community interface.
    
    This component structures all AI outputs into a consistent format
    ready for UI consumption and user presentation.
    """
    
    def __init__(self):
        """Initialize the output formatting API."""
        self.supported_languages = ["en", "hi", "gu"]  # English, Hindi, Gujarati
        logger.info("OutputFormattingAPI initialized")
    
    def format_case_report(self, case_id: str, ai_outputs: Dict, 
                          language: str = "en") -> Dict:
        """
        Format complete case report with all AI interpretations.
        
        Args:
            case_id: Case identifier
            ai_outputs: All AI-generated content including:
                - interpretations: Evidence interpretations
                - risk_assessment: Risk scoring results
                - timeline_narrative: Timeline narrative
                - recommendations: Safety recommendations
            language: Target language code (en, hi, gu)
        
        Returns:
            dict: Formatted report ready for UI consumption
            
        Example:
            >>> formatter = OutputFormattingAPI()
            >>> report = formatter.format_case_report("case_001", ai_outputs)
            >>> print(report["sections"]["executive_summary"])
        """
        logger.info(f"Formatting case report for case_id: {case_id}, language: {language}")
        
        if language not in self.supported_languages:
            logger.warning(f"Unsupported language: {language}, defaulting to English")
            language = "en"
        
        try:
            # TODO: Apply multilingual translation if language != "en"
            # translated_outputs = self._translate_outputs(ai_outputs, language)
            
            # Format report sections
            report = {
                "case_id": case_id,
                "language": language,
                "generated_at": datetime.now().isoformat(),
                "sections": {
                    "executive_summary": self._format_executive_summary(ai_outputs),
                    "evidence_interpretation": self._format_evidence_interpretation(ai_outputs),
                    "timeline_narrative": self._format_timeline_narrative(ai_outputs),
                    "safety_recommendations": self._format_safety_recommendations(ai_outputs)
                },
                "metadata": self._format_metadata(ai_outputs)
            }
            
            logger.info(f"Successfully formatted case report for {case_id}")
            return report
            
        except Exception as e:
            logger.exception(f"Error formatting case report: {e}")
            return self._create_error_report(case_id, language, str(e))
    
    def get_case_report(self, case_id: str, language: str = "en") -> Dict:
        """
        Retrieve formatted case report.
        
        This is a placeholder for future implementation where reports
        might be cached or stored.
        
        Args:
            case_id: Case identifier
            language: Target language code
        
        Returns:
            dict: Formatted case report or error
        """
        logger.info(f"Retrieving case report for case_id: {case_id}")
        
        # TODO: Implement report retrieval from cache/storage
        # For now, return placeholder
        return {
            "status": "not_implemented",
            "message": "Report retrieval not yet implemented. Use format_case_report() instead.",
            "case_id": case_id,
            "language": language
        }
    
    def _format_executive_summary(self, ai_outputs: Dict) -> Dict:
        """
        Format executive summary section.
        
        Args:
            ai_outputs: All AI outputs
            
        Returns:
            dict: Formatted executive summary
        """
        risk_assessment = ai_outputs.get("risk_assessment", {})
        interpretations = ai_outputs.get("interpretations", [])
        
        # Extract key findings
        key_findings = []
        for interp in interpretations[:5]:  # Top 5 interpretations
            if interp.get("confidence", 0) > 70:
                key_findings.append({
                    "finding": interp.get("interpretation", ""),
                    "confidence": interp.get("confidence", 0)
                })
        
        # Generate threat summary
        threat_summary = self._generate_threat_summary(risk_assessment, interpretations)
        
        return {
            "threat_summary": threat_summary,
            "risk_assessment": {
                "risk_level": risk_assessment.get("risk_level", "Unknown"),
                "risk_score": risk_assessment.get("risk_score", 0),
                "confidence": risk_assessment.get("confidence", 0),
                "reasoning": risk_assessment.get("reasoning", "")
            },
            "key_findings": key_findings,
            "total_artefacts_analyzed": len(interpretations),
            "ai_generated": True
        }
    
    def _format_evidence_interpretation(self, ai_outputs: Dict) -> Dict:
        """
        Format evidence interpretation section.
        
        Args:
            ai_outputs: All AI outputs
            
        Returns:
            dict: Formatted evidence interpretations
        """
        interpretations = ai_outputs.get("interpretations", [])
        
        # Group interpretations by confidence level
        high_confidence = [i for i in interpretations if i.get("confidence", 0) >= 80]
        medium_confidence = [i for i in interpretations if 60 <= i.get("confidence", 0) < 80]
        low_confidence = [i for i in interpretations if i.get("confidence", 0) < 60]
        
        return {
            "artefacts": interpretations,
            "summary": {
                "total_count": len(interpretations),
                "high_confidence_count": len(high_confidence),
                "medium_confidence_count": len(medium_confidence),
                "low_confidence_count": len(low_confidence),
                "average_confidence": self._calculate_average_confidence(interpretations)
            },
            "ai_generated": True
        }
    
    def _format_timeline_narrative(self, ai_outputs: Dict) -> Dict:
        """
        Format timeline narrative section.
        
        Args:
            ai_outputs: All AI outputs
            
        Returns:
            dict: Formatted timeline narrative
        """
        timeline_narrative = ai_outputs.get("timeline_narrative", {})
        
        return {
            "narrative": timeline_narrative.get("narrative", ""),
            "key_events": timeline_narrative.get("key_events", []),
            "patterns": timeline_narrative.get("patterns", []),
            "gaps": timeline_narrative.get("gaps", []),
            "confidence": timeline_narrative.get("confidence", 0),
            "event_count": timeline_narrative.get("event_count", 0),
            "ai_generated": True
        }
    
    def _format_safety_recommendations(self, ai_outputs: Dict) -> Dict:
        """
        Format safety recommendations section.
        
        Args:
            ai_outputs: All AI outputs
            
        Returns:
            dict: Formatted safety recommendations
        """
        recommendations = ai_outputs.get("recommendations", {})
        
        return {
            "recommendations": recommendations.get("recommendations", []),
            "priority": recommendations.get("priority", "Medium"),
            "disclaimer": recommendations.get("disclaimer", ""),
            "ai_generated": True
        }
    
    def _format_metadata(self, ai_outputs: Dict) -> Dict:
        """
        Format report metadata.
        
        Args:
            ai_outputs: All AI outputs
            
        Returns:
            dict: Formatted metadata
        """
        # TODO: Track actual AI models used
        ai_models_used = ["placeholder-model"]
        
        # Calculate processing statistics
        interpretations = ai_outputs.get("interpretations", [])
        avg_confidence = self._calculate_average_confidence(interpretations)
        
        return {
            "ai_models_used": ai_models_used,
            "processing_time_seconds": 0.0,  # TODO: Track actual processing time
            "confidence_average": avg_confidence,
            "components_executed": list(ai_outputs.keys()),
            "report_version": "1.0"
        }
    
    def _generate_threat_summary(self, risk_assessment: Dict, interpretations: List[Dict]) -> str:
        """
        Generate a one-line threat summary in plain language.
        
        Args:
            risk_assessment: Risk assessment data
            interpretations: List of interpretations
            
        Returns:
            str: Plain-language threat summary
        """
        risk_level = risk_assessment.get("risk_level", "Unknown")
        risk_score = risk_assessment.get("risk_score", 0)
        
        # Identify primary threat type from interpretations
        threat_indicators = {
            "stalkerware": 0,
            "tracking": 0,
            "malware": 0,
            "permission_abuse": 0,
            "surveillance": 0
        }
        
        for interp in interpretations:
            text = interp.get("interpretation", "").lower()
            original = str(interp.get("original", {})).lower()
            
            if "stalkerware" in text or "stalkerware" in original:
                threat_indicators["stalkerware"] += 2
            if "tracking" in text or "location" in text:
                threat_indicators["tracking"] += 1
            if "malware" in text or "malicious" in text:
                threat_indicators["malware"] += 2
            if "permission" in text and ("excessive" in text or "suspicious" in text):
                threat_indicators["permission_abuse"] += 1
            if "surveillance" in text or "monitoring" in text or "covert" in text:
                threat_indicators["surveillance"] += 1
        
        # Determine primary threat
        primary_threat = max(threat_indicators, key=threat_indicators.get)
        threat_count = threat_indicators[primary_threat]
        
        # Generate summary based on risk level and primary threat
        if risk_level == "Critical" or risk_score >= 90:
            if primary_threat == "stalkerware" and threat_count > 0:
                return "Critical threat detected: Device shows strong indicators of stalkerware installation and active surveillance."
            elif primary_threat == "malware" and threat_count > 0:
                return "Critical threat detected: Malicious software identified with potential for unauthorized device access."
            else:
                return "Critical security threat detected: Multiple high-risk indicators suggest immediate attention required."
        
        elif risk_level == "High" or risk_score >= 70:
            if primary_threat == "stalkerware" and threat_count > 0:
                return "High-risk threat: Potential stalkerware detected with location tracking and data access capabilities."
            elif primary_threat == "tracking" and threat_count > 0:
                return "High-risk threat: Suspicious location tracking activity detected with privacy implications."
            elif primary_threat == "surveillance" and threat_count > 0:
                return "High-risk threat: Device shows signs of unauthorized surveillance or monitoring activity."
            elif primary_threat == "permission_abuse" and threat_count > 0:
                return "High-risk threat: Applications detected with excessive permissions for sensitive data access."
            else:
                return "High-risk security concerns identified requiring investigation and potential remediation."
        
        elif risk_level == "Medium" or risk_score >= 40:
            if threat_count > 0:
                return "Moderate security concerns detected: Some suspicious patterns identified that warrant review."
            else:
                return "Moderate risk level: Device shows some anomalies that may require attention."
        
        else:
            return "Low risk detected: No significant security threats identified in forensic analysis."
    
    def _calculate_average_confidence(self, interpretations: List[Dict]) -> float:
        """
        Calculate average confidence across interpretations.
        
        Args:
            interpretations: List of interpretation results
            
        Returns:
            float: Average confidence (0-100)
        """
        if not interpretations:
            return 0.0
        
        confidences = [i.get("confidence", 0) for i in interpretations]
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def _translate_outputs(self, ai_outputs: Dict, target_language: str) -> Dict:
        """
        Translate AI outputs to target language.
        
        This is a placeholder for future multilingual integration.
        
        Args:
            ai_outputs: AI outputs in English
            target_language: Target language code
            
        Returns:
            dict: Translated outputs
        """
        # TODO: Integrate with multilingual translation module
        # This will be implemented when the translation API is ready
        
        logger.info(f"Translation to {target_language} not yet implemented")
        return ai_outputs
    
    def _create_error_report(self, case_id: str, language: str, 
                            error_message: str) -> Dict:
        """
        Create error report when formatting fails.
        
        Args:
            case_id: Case identifier
            language: Target language
            error_message: Error description
            
        Returns:
            dict: Error report
        """
        return {
            "case_id": case_id,
            "language": language,
            "generated_at": datetime.now().isoformat(),
            "status": "error",
            "error_message": error_message,
            "sections": {
                "executive_summary": {
                    "error": "Report formatting failed",
                    "ai_generated": True
                }
            },
            "metadata": {
                "error": True,
                "report_version": "1.0"
            }
        }
    
    def export_report_json(self, report: Dict, filepath: str) -> bool:
        """
        Export formatted report to JSON file.
        
        Args:
            report: Formatted report dictionary
            filepath: Output file path
            
        Returns:
            bool: Success status
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report exported to {filepath}")
            return True
        except Exception as e:
            logger.exception(f"Error exporting report: {e}")
            return False
    
    def validate_report_structure(self, report: Dict) -> tuple:
        """
        Validate report structure for completeness.
        
        Args:
            report: Formatted report
            
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required top-level keys
        required_keys = ["case_id", "language", "generated_at", "sections", "metadata"]
        for key in required_keys:
            if key not in report:
                errors.append(f"Missing required key: {key}")
        
        # Check sections
        if "sections" in report:
            required_sections = [
                "executive_summary",
                "evidence_interpretation",
                "timeline_narrative",
                "safety_recommendations"
            ]
            for section in required_sections:
                if section not in report["sections"]:
                    errors.append(f"Missing required section: {section}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
