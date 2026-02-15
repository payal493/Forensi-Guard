"""
Forensic Artefact Ingestion API

Receives and validates forensic data from the existing Forensi-Guard engine.
Operates in read-only mode to preserve evidence integrity.
"""

import logging
from typing import Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class ForensicArtefactIngestionAPI:
    """
    API for ingesting forensic data from the existing forensic engine.
    
    This component validates data structure and prepares it for AI processing
    without modifying the original evidence.
    """
    
    def __init__(self):
        """Initialize the ingestion API."""
        self.supported_artefact_types = ["sms", "call", "app", "media", "finding"]
        logger.info("ForensicArtefactIngestionAPI initialized")
    
    def ingest_case_data(self, case_id: str, forensic_data: Dict) -> Dict:
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
            
        Example:
            >>> api = ForensicArtefactIngestionAPI()
            >>> result = api.ingest_case_data("case_001", forensic_data)
            >>> print(result["status"])
            "success"
        """
        logger.info(f"Ingesting case data for case_id: {case_id}")
        
        try:
            # Validate forensic data structure
            is_valid, errors = self.validate_forensic_data(forensic_data)
            
            if not is_valid:
                logger.error(f"Validation failed for case {case_id}: {errors}")
                return {
                    "status": "validation_failed",
                    "case_id": case_id,
                    "errors": errors,
                    "timestamp": datetime.now().isoformat()
                }
            
            # TODO: Store validated data in temporary read-only cache
            # This ensures original evidence is never modified
            
            logger.info(f"Successfully ingested case data for {case_id}")
            return {
                "status": "success",
                "case_id": case_id,
                "artefact_count": self._count_artefacts(forensic_data),
                "timestamp": datetime.now().isoformat(),
                "validation_passed": True
            }
            
        except Exception as e:
            logger.exception(f"Error ingesting case data for {case_id}")
            return {
                "status": "error",
                "case_id": case_id,
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_forensic_data(self, forensic_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate forensic data structure and integrity.
        
        Args:
            forensic_data: Forensic data dictionary to validate
        
        Returns:
            tuple: (is_valid, list_of_errors)
            
        Example:
            >>> api = ForensicArtefactIngestionAPI()
            >>> is_valid, errors = api.validate_forensic_data(data)
            >>> if not is_valid:
            ...     print(f"Validation errors: {errors}")
        """
        errors = []
        
        # Check required top-level keys
        required_keys = ["metadata", "timeline", "findings", "hashes"]
        for key in required_keys:
            if key not in forensic_data:
                errors.append(f"Missing required key: {key}")
        
        # Validate metadata structure
        if "metadata" in forensic_data:
            metadata = forensic_data["metadata"]
            if not isinstance(metadata, dict):
                errors.append("metadata must be a dictionary")
            else:
                # Check for essential metadata fields
                if "case_name" not in metadata:
                    errors.append("metadata missing 'case_name'")
                if "device_type" not in metadata:
                    errors.append("metadata missing 'device_type'")
        
        # Validate timeline structure
        if "timeline" in forensic_data:
            timeline = forensic_data["timeline"]
            if not isinstance(timeline, dict):
                errors.append("timeline must be a dictionary")
            elif "events" not in timeline:
                errors.append("timeline missing 'events' list")
        
        # Validate findings structure
        if "findings" in forensic_data:
            findings = forensic_data["findings"]
            if not isinstance(findings, dict):
                errors.append("findings must be a dictionary")
        
        # Validate hashes structure
        if "hashes" in forensic_data:
            hashes = forensic_data["hashes"]
            if not isinstance(hashes, dict):
                errors.append("hashes must be a dictionary")
            elif "algorithm" not in hashes:
                errors.append("hashes missing 'algorithm' field")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info("Forensic data validation passed")
        else:
            logger.warning(f"Forensic data validation failed: {errors}")
        
        return is_valid, errors
    
    def _count_artefacts(self, forensic_data: Dict) -> int:
        """
        Count total number of artefacts in forensic data.
        
        Args:
            forensic_data: Validated forensic data
            
        Returns:
            int: Total artefact count
        """
        count = 0
        
        # Count timeline events
        if "timeline" in forensic_data and "events" in forensic_data["timeline"]:
            count += len(forensic_data["timeline"]["events"])
        
        # Count findings
        if "findings" in forensic_data:
            findings = forensic_data["findings"]
            for finding_type in findings.values():
                if isinstance(finding_type, list):
                    count += len(finding_type)
        
        return count
    
    def get_case_metadata(self, forensic_data: Dict) -> Dict:
        """
        Extract case metadata from forensic data.
        
        Args:
            forensic_data: Validated forensic data
            
        Returns:
            dict: Case metadata
        """
        return forensic_data.get("metadata", {})
