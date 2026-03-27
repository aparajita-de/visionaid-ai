# Hallucination detection & safety

import asyncio
from typing import Dict, Any, List
import hashlib
import json

class GuardrailService:
    def __init__(self):
        # Gold standard database simulation
        self.gold_standard_db = {
            "pneumonia": ["fever", "cough", "chest pain", "consolidation"],
            "tuberculosis": ["cough", "weight loss", "night sweats", "cavitary lesion"],
            "fracture": ["pain", "swelling", "deformity", "bone discontinuity"],
            "normal": ["clear lung fields", "no acute findings"]
        }
        
    async def validate(self, diagnosis: Dict[str, Any], 
                      image_bytes: bytes) -> Dict[str, Any]:
        """
        Validate AI output against gold standard databases
        Detect and prevent hallucinations
        """
        validation_results = {
            "confidence": 0.0,
            "hallucination_detected": False,
            "hallucinations": [],
            "verified_findings": [],
            "safety_score": 0.0
        }
        
        findings = diagnosis.get("findings", [])
        
        # Cross-reference with gold standard
        for finding in findings:
            finding_text = finding["finding"].lower()
            verified = False
            
            # Check against gold standard
            for condition, keywords in self.gold_standard_db.items():
                if any(keyword in finding_text for keyword in keywords):
                    verified = True
                    validation_results["verified_findings"].append({
                        "finding": finding,
                        "matched_condition": condition
                    })
                    break
            
            if not verified:
                validation_results["hallucination_detected"] = True
                validation_results["hallucinations"].append(finding)
        
        # Calculate confidence score based on verification
        total_findings = len(findings) or 1
        verified_count = len(validation_results["verified_findings"])
        validation_results["confidence"] = verified_count / total_findings
        
        # Calculate safety score
        validation_results["safety_score"] = validation_results["confidence"] * 100
        
        # Add clinical safety warnings
        if validation_results["hallucination_detected"]:
            validation_results["warnings"] = [
                "Some findings could not be verified against medical databases",
                "Manual review by qualified professional is strongly recommended"
            ]
        else:
            validation_results["warnings"] = []
            
        # Add disclaimer
        validation_results["disclaimer"] = (
            "This is an AI-assisted preliminary analysis. "
            "All findings require clinical correlation and verification by a qualified healthcare professional."
        )
        
        return validation_results
    
    async def check_confidence_threshold(self, confidence: float) -> bool:
        """Check if confidence meets safety threshold"""
        return confidence >= 0.70  # 70% confidence threshold