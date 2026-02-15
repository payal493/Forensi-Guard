"""
AI Safety Advisor

Generates advisory-only safety recommendations based on forensic findings.
Provides actionable guidance while maintaining advisory (non-authoritative) status.
"""

import logging
from typing import Dict, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class AISafetyAdvisor:
    """
    Generates safety recommendations based on forensic analysis.
    
    This component provides advisory-only recommendations to help users
    take protective actions based on findings. All advice is clearly marked
    as advisory and not authoritative.
    """
    
    def __init__(self):
        """Initialize the safety advisor."""
        self.recommendation_categories = [
            "Immediate Action",
            "Preventive Measures",
            "Professional Help",
            "Evidence Preservation"
        ]
        
        self.priority_levels = ["Low", "Medium", "High", "Urgent"]
        
        logger.info("AISafetyAdvisor initialized")
    
    def generate_recommendations(self, risk_assessment: Dict, findings: List[Dict]) -> Dict:
        """
        Generate safety recommendations based on findings.
        
        Args:
            risk_assessment: Risk scoring output from AIRiskScoringEngine
            findings: Analysis findings from forensic engine
        
        Returns:
            dict: {
                "recommendations": list[dict],
                "priority": str (Low/Medium/High/Urgent),
                "disclaimer": str,
                "ai_generated": True
            }
            
        Example:
            >>> advisor = AISafetyAdvisor()
            >>> recommendations = advisor.generate_recommendations(risk_data, findings)
            >>> for rec in recommendations["recommendations"]:
            ...     print(f"{rec['action']}")
        """
        logger.info(f"Generating safety recommendations for {len(findings)} findings")
        
        try:
            # TODO: Implement AI-based recommendation generation
            # This should use ML models to generate contextual advice
            
            # Generate recommendations based on risk level
            risk_level = risk_assessment.get("risk_level", "Medium")
            recommendations = self._generate_recommendations_by_risk(risk_level, findings)
            
            # Prioritize recommendations
            prioritized = self.prioritize_recommendations(recommendations)
            
            # Determine overall priority
            overall_priority = self._determine_overall_priority(risk_level, findings)
            
            # Generate disclaimer
            disclaimer = self._generate_disclaimer()
            
            result = {
                "recommendation_id": str(uuid.uuid4()),
                "recommendations": prioritized,
                "priority": overall_priority,
                "disclaimer": disclaimer,
                "risk_level": risk_level,
                "ai_generated": True,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Generated {len(prioritized)} recommendations with priority: {overall_priority}")
            return result
            
        except Exception as e:
            logger.exception(f"Error generating recommendations: {e}")
            return self._create_error_response(risk_assessment, findings, str(e))
    
    def prioritize_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Sort recommendations by urgency and impact.
        
        Args:
            recommendations: List of recommendation dictionaries
        
        Returns:
            list: Sorted recommendations (highest priority first)
            
        Example:
            >>> advisor = AISafetyAdvisor()
            >>> sorted_recs = advisor.prioritize_recommendations(recommendations)
        """
        # Priority order: Urgent > High > Medium > Low
        priority_order = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 3}
        
        # Category order: Immediate > Professional > Preventive > Evidence
        category_order = {
            "Immediate Action": 0,
            "Professional Help": 1,
            "Preventive Measures": 2,
            "Evidence Preservation": 3
        }
        
        def sort_key(rec):
            priority = priority_order.get(rec.get("priority", "Low"), 4)
            category = category_order.get(rec.get("category", "Preventive Measures"), 4)
            return (priority, category)
        
        return sorted(recommendations, key=sort_key)
    
    def _generate_recommendations_by_risk(self, risk_level: str, 
                                         findings: List[Dict]) -> List[Dict]:
        """
        Generate recommendations based on risk level.
        
        Args:
            risk_level: Risk level (Low/Medium/High/Critical)
            findings: Forensic findings
            
        Returns:
            list: Generated recommendations
        """
        recommendations = []
        
        # TODO: Implement AI-based contextual recommendation generation
        # This should analyze findings and generate specific advice
        
        # Placeholder recommendations based on risk level
        if risk_level in ["High", "Critical"]:
            recommendations.extend(self._get_high_risk_recommendations(findings))
        elif risk_level == "Medium":
            recommendations.extend(self._get_medium_risk_recommendations(findings))
        else:
            recommendations.extend(self._get_low_risk_recommendations(findings))
        
        # Add general recommendations
        recommendations.extend(self._get_general_recommendations())
        
        return recommendations
    
    def _get_high_risk_recommendations(self, findings: List[Dict]) -> List[Dict]:
        """Generate recommendations for high/critical risk scenarios."""
        return [
            {
                "category": "Immediate Action",
                "priority": "Urgent",
                "action": "Review and disable suspicious applications immediately",
                "reasoning": "High-risk indicators suggest potential malicious activity",
                "steps": [
                    "Go to Settings > Apps on your device",
                    "Review recently installed applications",
                    "Disable or uninstall any unfamiliar apps",
                    "Pay special attention to apps with excessive permissions"
                ]
            },
            {
                "category": "Professional Help",
                "priority": "High",
                "action": "Contact local cyber harassment support services or law enforcement",
                "reasoning": "The severity of findings suggests professional intervention may be needed",
                "steps": [
                    "Document all suspicious activities",
                    "Preserve evidence by not deleting suspicious apps",
                    "Contact local cyber crime unit or support organization",
                    "Consider consulting with a cybersecurity professional"
                ]
            },
            {
                "category": "Evidence Preservation",
                "priority": "High",
                "action": "Preserve device evidence for potential legal proceedings",
                "reasoning": "Evidence integrity is crucial for any future legal action",
                "steps": [
                    "Do not factory reset your device",
                    "Keep the device powered on and charged",
                    "Document any suspicious messages or calls",
                    "Save this forensic report securely"
                ]
            }
        ]
    
    def _get_medium_risk_recommendations(self, findings: List[Dict]) -> List[Dict]:
        """Generate recommendations for medium risk scenarios."""
        return [
            {
                "category": "Immediate Action",
                "priority": "Medium",
                "action": "Review app permissions and revoke unnecessary access",
                "reasoning": "Some applications have permissions that may pose privacy risks",
                "steps": [
                    "Go to Settings > Apps > Permissions",
                    "Review which apps have access to location, contacts, and messages",
                    "Revoke permissions that seem unnecessary for app functionality"
                ]
            },
            {
                "category": "Preventive Measures",
                "priority": "Medium",
                "action": "Enable additional security features on your device",
                "reasoning": "Strengthening device security can prevent future issues",
                "steps": [
                    "Enable screen lock with strong PIN or biometric",
                    "Turn on Google Play Protect",
                    "Enable two-factor authentication for important accounts",
                    "Keep your device software up to date"
                ]
            }
        ]
    
    def _get_low_risk_recommendations(self, findings: List[Dict]) -> List[Dict]:
        """Generate recommendations for low risk scenarios."""
        return [
            {
                "category": "Preventive Measures",
                "priority": "Low",
                "action": "Maintain good security hygiene practices",
                "reasoning": "Regular security practices help prevent future issues",
                "steps": [
                    "Regularly review installed applications",
                    "Only install apps from trusted sources",
                    "Keep your device operating system updated",
                    "Be cautious about granting app permissions"
                ]
            }
        ]
    
    def _get_general_recommendations(self) -> List[Dict]:
        """Generate general recommendations applicable to all cases."""
        return [
            {
                "category": "Evidence Preservation",
                "priority": "Medium",
                "action": "Keep a copy of this forensic report",
                "reasoning": "Documentation may be useful for future reference or legal purposes",
                "steps": [
                    "Save this report in a secure location",
                    "Consider keeping both digital and printed copies",
                    "Do not share the report publicly or on social media"
                ]
            },
            {
                "category": "Professional Help",
                "priority": "Low",
                "action": "Consider consulting with cybersecurity or legal professionals if concerns persist",
                "reasoning": "Professional guidance can provide additional peace of mind",
                "steps": [
                    "Research local cybersecurity consultants",
                    "Contact legal aid organizations if needed",
                    "Reach out to cyber harassment support groups"
                ]
            }
        ]
    
    def _determine_overall_priority(self, risk_level: str, findings: List[Dict]) -> str:
        """
        Determine overall priority level for recommendations.
        
        Args:
            risk_level: Risk assessment level
            findings: Forensic findings
            
        Returns:
            str: Overall priority (Low/Medium/High/Urgent)
        """
        priority_mapping = {
            "Critical": "Urgent",
            "High": "High",
            "Medium": "Medium",
            "Low": "Low"
        }
        
        return priority_mapping.get(risk_level, "Medium")
    
    def _generate_disclaimer(self) -> str:
        """
        Generate advisory disclaimer for recommendations.
        
        Returns:
            str: Disclaimer text
        """
        return (
            "ADVISORY NOTICE: These recommendations are advisory only and generated by AI "
            "based on forensic analysis. They are not authoritative legal or security advice. "
            "For legal concerns, safety issues, or professional guidance, please consult with "
            "law enforcement, legal professionals, or certified cybersecurity experts. "
            "This system does not modify device data or forensic evidence."
        )
    
    def _create_error_response(self, risk_assessment: Dict, findings: List[Dict], 
                               error_message: str) -> Dict:
        """
        Create error response for failed recommendation generation.
        
        Args:
            risk_assessment: Risk assessment data
            findings: Forensic findings
            error_message: Error description
            
        Returns:
            dict: Error response
        """
        return {
            "recommendation_id": str(uuid.uuid4()),
            "recommendations": [
                {
                    "category": "Professional Help",
                    "priority": "Medium",
                    "action": "Consult with a cybersecurity professional",
                    "reasoning": f"Automated recommendation generation encountered an error: {error_message}",
                    "steps": [
                        "Review the forensic findings manually",
                        "Contact a cybersecurity expert for guidance",
                        "Preserve all evidence for professional analysis"
                    ]
                }
            ],
            "priority": "Medium",
            "disclaimer": self._generate_disclaimer(),
            "ai_generated": True,
            "error": True,
            "generated_at": datetime.now().isoformat()
        }
