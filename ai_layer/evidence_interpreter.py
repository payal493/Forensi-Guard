"""
AI Evidence Interpreter

Converts technical forensic artefacts into plain-language explanations.
Uses AI models to generate human-readable interpretations while maintaining
technical accuracy.
"""

import logging
from typing import Dict, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class AIEvidenceInterpreter:
    """
    Interprets forensic artefacts and generates plain-language explanations.
    
    This component uses AI models (to be implemented) to convert technical
    forensic data into accessible narratives for non-technical users.
    """
    
    def __init__(self):
        """Initialize the evidence interpreter."""
        self.supported_types = ["sms", "call", "app", "media", "finding"]
        # TODO: Initialize AI model (e.g., local LLM like Llama 2 7B or Mistral 7B)
        # self.model = load_local_llm()
        logger.info("AIEvidenceInterpreter initialized")
    
    def interpret_artefact(self, artefact: Dict, artefact_type: str) -> Dict:
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
            
        Example:
            >>> interpreter = AIEvidenceInterpreter()
            >>> result = interpreter.interpret_artefact(
            ...     {"app": "tracker", "permission": "LOCATION"},
            ...     "app"
            ... )
            >>> print(result["interpretation"])
        """
        logger.info(f"Interpreting artefact of type: {artefact_type}")
        
        if artefact_type not in self.supported_types:
            logger.warning(f"Unsupported artefact type: {artefact_type}")
            return self._create_error_response(artefact, artefact_type)
        
        try:
            # TODO: Implement actual AI interpretation using local LLM
            # interpretation = self._generate_interpretation(artefact, artefact_type)
            # confidence = self._calculate_confidence(interpretation)
            # reasoning = self._generate_reasoning(artefact, interpretation)
            # alternatives = self._generate_alternatives(artefact, artefact_type)
            
            # Placeholder implementation
            interpretation = self._placeholder_interpretation(artefact, artefact_type)
            
            return {
                "interpretation_id": str(uuid.uuid4()),
                "original": artefact,
                "interpretation": interpretation["text"],
                "confidence": interpretation["confidence"],
                "reasoning": interpretation["reasoning"],
                "alternatives": interpretation["alternatives"],
                "artefact_type": artefact_type,
                "ai_generated": True,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.exception(f"Error interpreting artefact: {e}")
            return self._create_error_response(artefact, artefact_type, str(e))
    
    def batch_interpret(self, artefacts: List[Dict]) -> List[Dict]:
        """
        Interpret multiple artefacts efficiently.
        
        Args:
            artefacts: List of (artefact, artefact_type) tuples
        
        Returns:
            list: List of interpretation results
            
        Example:
            >>> interpreter = AIEvidenceInterpreter()
            >>> artefacts = [
            ...     ({"type": "sms", "content": "..."}, "sms"),
            ...     ({"type": "call", "duration": 120}, "call")
            ... ]
            >>> results = interpreter.batch_interpret(artefacts)
        """
        logger.info(f"Batch interpreting {len(artefacts)} artefacts")
        
        results = []
        for artefact_data, artefact_type in artefacts:
            result = self.interpret_artefact(artefact_data, artefact_type)
            results.append(result)
        
        logger.info(f"Completed batch interpretation of {len(results)} artefacts")
        return results
    
    def _placeholder_interpretation(self, artefact: Dict, artefact_type: str) -> Dict:
        """
        Generate mock interpretation using rule-based logic.
        
        TODO: Replace this with actual AI model (local LLM like Llama 2 7B or Mistral 7B)
        Future implementation should:
        - Load pre-trained LLM model
        - Use prompt engineering with forensic context
        - Generate contextual interpretations based on artefact content
        - Calculate confidence using model perplexity
        
        Args:
            artefact: Forensic artefact data
            artefact_type: Type of artefact
            
        Returns:
            dict: Mock interpretation data
        """
        # MOCK AI LOGIC: Rule-based interpretation
        # This simulates what an AI model would do
        
        # Extract key information from artefact
        artefact_str = str(artefact).lower()
        
        # Check for specific patterns and generate contextual interpretations
        if artefact_type == "app":
            return self._interpret_app_artefact(artefact)
        elif artefact_type == "sms":
            return self._interpret_sms_artefact(artefact)
        elif artefact_type == "call":
            return self._interpret_call_artefact(artefact)
        elif artefact_type == "media":
            return self._interpret_media_artefact(artefact)
        elif artefact_type == "finding":
            return self._interpret_finding_artefact(artefact)
        else:
            return {
                "text": "A forensic artefact was identified and preserved for analysis.",
                "confidence": 60.0,
                "reasoning": "Artefact type requires specialized interpretation.",
                "alternatives": []
            }
    
    def _interpret_app_artefact(self, artefact: Dict) -> Dict:
        """Mock interpretation for app artefacts."""
        # Extract app details with forensic precision
        app_name = artefact.get("app", artefact.get("package_name", "unknown app"))
        permissions = artefact.get("permissions", [])
        permission = artefact.get("permission", "")
        granted = artefact.get("granted", None)
        
        # Get metadata for additional context
        metadata = artefact.get("metadata", {})
        if not app_name or app_name == "unknown app":
            app_name = metadata.get("app", metadata.get("package_name", "unknown app"))
        if not permissions:
            permissions = metadata.get("permissions", [])
        if not permission:
            permission = metadata.get("permission", "")
        
        # Build permission list for display
        permission_list = []
        if permissions and isinstance(permissions, list):
            permission_list = permissions
        elif permission:
            permission_list = [permission]
        
        # Rule-based interpretation logic with forensic specificity
        if "location" in str(permissions).lower() or "location" in permission.lower():
            # Determine specific permission type
            if "FINE_LOCATION" in str(permissions) or "FINE_LOCATION" in permission:
                location_type = "precise GPS location"
                precision = "exact coordinates"
            elif "COARSE_LOCATION" in str(permissions) or "COARSE_LOCATION" in permission:
                location_type = "approximate location"
                precision = "general area based on network towers"
            else:
                location_type = "device location"
                precision = "GPS or network data"
            
            granted_text = f" Permission was granted." if granted else ""
            
            return {
                "text": f"The app {app_name} has permission to access your {location_type}. "
                        f"This allows the app to track your {precision}.{granted_text}",
                "confidence": 87.0,
                "reasoning": f"Location permission detected: {permission or permissions}. This is a privacy-sensitive permission that enables location tracking.",
                "alternatives": [
                    {
                        "interpretation": f"The app {app_name} may use location for legitimate features like navigation, weather, or local services.",
                        "confidence": 72.0
                    }
                ]
            }
        elif "contact" in str(permissions).lower() or "contact" in permission.lower():
            granted_text = f" Permission was granted." if granted else ""
            
            return {
                "text": f"The app {app_name} has permission to access your contact list. "
                        f"This includes names, phone numbers, and email addresses stored on your device.{granted_text}",
                "confidence": 84.0,
                "reasoning": f"Contacts permission detected: {permission or 'READ_CONTACTS'}. This allows the app to read your entire contact database.",
                "alternatives": []
            }
        elif "sms" in str(permissions).lower() or "message" in str(permissions).lower():
            granted_text = f" Permission was granted." if granted else ""
            
            return {
                "text": f"The app {app_name} has permission to read your text messages. "
                        f"This is a sensitive permission that provides access to private SMS communications.{granted_text}",
                "confidence": 89.0,
                "reasoning": f"SMS/messaging permission detected: {permission or 'READ_SMS'}. This is considered high-risk for privacy.",
                "alternatives": []
            }
        elif "camera" in str(permissions).lower():
            granted_text = f" Permission was granted." if granted else ""
            
            return {
                "text": f"The app {app_name} has permission to access your device camera. "
                        f"This allows it to capture photos and videos.{granted_text}",
                "confidence": 82.0,
                "reasoning": "Camera permission detected. This enables photo and video capture.",
                "alternatives": []
            }
        elif permission_list:
            # Multiple permissions or specific permission granted
            perm_text = ", ".join(permission_list) if len(permission_list) <= 3 else f"{len(permission_list)} permissions"
            granted_text = f" Permission was granted." if granted else ""
            
            return {
                "text": f"The app {app_name} has been granted access to: {perm_text}.{granted_text}",
                "confidence": 78.0,
                "reasoning": f"App detected with specific permissions: {perm_text}.",
                "alternatives": []
            }
        else:
            return {
                "text": f"The app {app_name} is installed on the device.",
                "confidence": 75.0,
                "reasoning": "App installation detected in forensic analysis.",
                "alternatives": []
            }
    
    def _interpret_sms_artefact(self, artefact: Dict) -> Dict:
        """Mock interpretation for SMS artefacts."""
        # Check both top-level and metadata for fields
        metadata = artefact.get("metadata", {})
        sender = artefact.get("sender") or metadata.get("sender") or metadata.get("address", "unknown number")
        content = artefact.get("content") or metadata.get("content") or metadata.get("body", "")
        timestamp = artefact.get("timestamp", "")
        
        # Format timestamp if available
        time_text = f" at {timestamp}" if timestamp else ""
        
        # Check for suspicious patterns
        if any(word in content.lower() for word in ["password", "otp", "code", "verify"]):
            return {
                "text": f"SMS from sender {sender}{time_text} contains authentication-related content (passwords, OTP codes, or verification tokens). "
                        f"This message type is commonly targeted in phishing or account takeover attempts.",
                "confidence": 85.0,
                "reasoning": f"Message from {sender} contains security-sensitive keywords indicating authentication data.",
                "alternatives": []
            }
        else:
            return {
                "text": f"SMS artefact from sender {sender}{time_text} was recovered from device storage.",
                "confidence": 80.0,
                "reasoning": f"SMS record extracted from device database. Sender: {sender}.",
                "alternatives": []
            }
    
    def _interpret_call_artefact(self, artefact: Dict) -> Dict:
        """Mock interpretation for call artefacts."""
        # Check both top-level and metadata for fields
        metadata = artefact.get("metadata", {})
        number = artefact.get("number") or metadata.get("number") or metadata.get("address", "unknown number")
        duration = artefact.get("duration") or metadata.get("duration", 0)
        call_type = artefact.get("type") or metadata.get("type", "unknown")
        timestamp = artefact.get("timestamp", "")
        
        # Format duration more clearly
        if duration > 0:
            minutes = duration // 60
            seconds = duration % 60
            if minutes > 0:
                duration_text = f"{minutes} minute(s) {seconds} second(s)"
            else:
                duration_text = f"{seconds} second(s)"
        else:
            duration_text = "0 seconds (call not answered or missed)"
        
        # Format call type
        type_map = {
            "incoming": "incoming call",
            "outgoing": "outgoing call",
            "missed": "missed call",
            "rejected": "rejected call"
        }
        call_type_text = type_map.get(call_type.lower(), call_type)
        
        time_text = f" at {timestamp}" if timestamp else ""
        
        return {
            "text": f"Call log entry: {call_type_text} with number {number}{time_text}. "
                    f"Duration: {duration_text}.",
            "confidence": 88.0,
            "reasoning": f"Call record extracted from device call log. Number: {number}, Type: {call_type}, Duration: {duration}s.",
            "alternatives": []
        }
    
    def _interpret_media_artefact(self, artefact: Dict) -> Dict:
        """Mock interpretation for media artefacts."""
        # Check both top-level and metadata for fields
        metadata = artefact.get("metadata", {})
        filename = artefact.get("filename") or metadata.get("filename") or metadata.get("name", "unknown file")
        location = artefact.get("location", {}) or metadata.get("location", {})
        timestamp = artefact.get("timestamp", "")
        
        # Check for GPS coordinates in location or metadata
        gps_lat = location.get("latitude") or metadata.get("gps_latitude")
        gps_lon = location.get("longitude") or metadata.get("gps_longitude")
        
        time_text = f" captured at {timestamp}" if timestamp else ""
        
        if gps_lat and gps_lon:
            return {
                "text": f"Media file '{filename}'{time_text} contains embedded GPS metadata. "
                        f"Coordinates: {gps_lat}, {gps_lon}. This indicates the precise location where the photo or video was captured.",
                "confidence": 85.0,
                "reasoning": f"Media file contains GPS EXIF metadata with coordinates ({gps_lat}, {gps_lon}).",
                "alternatives": []
            }
        elif location or gps_lat or gps_lon:
            return {
                "text": f"Media file '{filename}'{time_text} contains location metadata indicating where the content was captured.",
                "confidence": 82.0,
                "reasoning": "Media file contains partial location data in EXIF metadata.",
                "alternatives": []
            }
        else:
            return {
                "text": f"Media file '{filename}'{time_text} was recovered from device storage. No GPS metadata detected.",
                "confidence": 78.0,
                "reasoning": "Media file metadata extracted from device storage without location data.",
                "alternatives": []
            }
    
    def _interpret_finding_artefact(self, artefact: Dict) -> Dict:
        """Mock interpretation for forensic findings."""
        finding_type = artefact.get("type", "unknown")
        description = artefact.get("description", "")
        severity = artefact.get("severity", "medium")
        indicators = artefact.get("indicators", [])
        
        # Map severity to forensic language
        severity_map = {
            "low": "low-priority observation",
            "medium": "moderate-risk indicator",
            "high": "high-risk security indicator",
            "critical": "critical security threat"
        }
        severity_text = severity_map.get(severity, "security indicator")
        
        # Build forensic interpretation based on finding type
        if "malware" in finding_type.lower() or "malicious" in description.lower():
            interpretation = f"Forensic analysis identified a {severity_text}: {description}. " \
                           f"This may indicate the presence of malicious software or unauthorized surveillance activity."
        elif "anomaly" in finding_type.lower() or "unusual" in description.lower():
            interpretation = f"Behavioral analysis detected a {severity_text}: {description}. " \
                           f"This pattern deviates from typical device usage and may warrant further investigation."
        elif "permission" in finding_type.lower() or "access" in description.lower():
            interpretation = f"Permission analysis flagged a {severity_text}: {description}. " \
                           f"This may indicate excessive or suspicious access to sensitive device resources."
        elif "tracking" in finding_type.lower() or "location" in description.lower():
            interpretation = f"Location tracking analysis identified a {severity_text}: {description}. " \
                           f"This may indicate covert monitoring activity or location surveillance."
        else:
            interpretation = f"Automated forensic analysis detected a {severity_text}: {description}. " \
                           f"This pattern was identified through rule-based anomaly detection."
        
        # Build reasoning with indicators if available
        reasoning_parts = [f"Finding type: {finding_type}", f"Severity: {severity}"]
        if indicators:
            reasoning_parts.append(f"Indicators: {', '.join(indicators[:3])}")
        reasoning = ". ".join(reasoning_parts) + "."
        
        return {
            "text": interpretation,
            "confidence": 75.0,
            "reasoning": reasoning,
            "alternatives": [
                {
                    "interpretation": "This pattern may represent legitimate application behavior depending on user context and device usage patterns.",
                    "confidence": 55.0
                }
            ]
        }
    
    def _create_error_response(self, artefact: Dict, artefact_type: str, 
                               error_message: str = None) -> Dict:
        """
        Create error response for failed interpretation.
        
        Args:
            artefact: Original artefact data
            artefact_type: Type of artefact
            error_message: Optional error message
            
        Returns:
            dict: Error response
        """
        return {
            "interpretation_id": str(uuid.uuid4()),
            "original": artefact,
            "interpretation": "Unable to generate interpretation for this artefact.",
            "confidence": 0.0,
            "reasoning": error_message or "Interpretation failed",
            "alternatives": [],
            "artefact_type": artefact_type,
            "ai_generated": True,
            "error": True,
            "generated_at": datetime.now().isoformat()
        }
    
    def get_interpretation_stats(self, interpretations: List[Dict]) -> Dict:
        """
        Calculate statistics for a batch of interpretations.
        
        Args:
            interpretations: List of interpretation results
            
        Returns:
            dict: Statistics including average confidence, error rate, etc.
        """
        if not interpretations:
            return {
                "total_count": 0,
                "average_confidence": 0.0,
                "error_count": 0,
                "error_rate": 0.0
            }
        
        total = len(interpretations)
        confidences = [i.get("confidence", 0.0) for i in interpretations]
        errors = sum(1 for i in interpretations if i.get("error", False))
        
        return {
            "total_count": total,
            "average_confidence": sum(confidences) / total if total > 0 else 0.0,
            "min_confidence": min(confidences) if confidences else 0.0,
            "max_confidence": max(confidences) if confidences else 0.0,
            "error_count": errors,
            "error_rate": (errors / total * 100) if total > 0 else 0.0
        }
