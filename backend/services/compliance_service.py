# ICD-10/CPT mapping

from typing import Dict, Any, List
import json

class ComplianceService:
    def __init__(self):
        # ICD-10 mapping database
        self.icd10_mapping = {
            "pneumonia": "J18.9",
            "tuberculosis": "A15.0",
            "fracture": "S32.9",
            "normal": "Z01.89",
            "pulmonary consolidation": "J18.9",
            "febrile state": "R50.9"
        }
        
        # CPT codes for procedures
        self.cpt_mapping = {
            "chest_xray": "71045",
            "ct_chest": "71250",
            "consultation": "99243",
            "follow_up": "99212"
        }
    
    async def map_to_codes(self, diagnosis: Dict[str, Any], 
                          confidence_score: float) -> Dict[str, Any]:
        """
        Map clinical findings to ICD-10 and CPT codes
        """
        findings = diagnosis.get("findings", [])
        
        icd10_codes = []
        cpt_codes = []
        
        # Map each finding to appropriate codes
        for finding in findings:
            finding_text = finding["finding"].lower()
            
            # Find matching ICD-10 code
            for condition, code in self.icd10_mapping.items():
                if condition in finding_text:
                    icd10_codes.append(code)
                    break
            
            # Add default if no match found
            if not icd10_codes:
                icd10_codes.append("R69")  # Unknown illness
            
        # Add CPT codes based on findings
        if any("chest" in f["finding"].lower() for f in findings):
            cpt_codes.append(self.cpt_mapping["chest_xray"])
        
        # Always add consultation code
        cpt_codes.append(self.cpt_mapping["consultation"])
        
        # Remove duplicates while preserving order
        icd10_codes = list(dict.fromkeys(icd10_codes))
        cpt_codes = list(dict.fromkeys(cpt_codes))
        
        return {
            "icd10": icd10_codes,
            "cpt": cpt_codes,
            "confidence_threshold_met": confidence_score >= 0.70,
            "requires_manual_review": confidence_score < 0.85
        }