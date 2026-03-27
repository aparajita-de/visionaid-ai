# Core diagnosis logic

import asyncio
import base64
from typing import Dict, Any, List
import requests
from PIL import Image
import io
import json

class DiagnosisService:
    def __init__(self):
        # Using open-source models via HuggingFace
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/biogpt"
        self.headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}  # User to add their token
        
    async def analyze(self, image_bytes: bytes, patient_age: int, 
                     patient_gender: str, symptoms: str, 
                     clinical_notes: str = None) -> Dict[str, Any]:
        """
        Perform multimodal analysis using vision-language models
        """
        # Simulate AI analysis with comprehensive medical reasoning
        # In production, this would call actual models like LLaVA-Med
        
        # Preprocess image for analysis
        image = Image.open(io.BytesIO(image_bytes))
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Enhanced clinical reasoning with contextual understanding
        findings = []
        recommendations = []
        critical_findings = []
        
        # Rule-based clinical reasoning (simulated)
        if "chest" in symptoms.lower() or "cough" in symptoms.lower():
            findings.append({
                "region": "lungs",
                "finding": "Possible pulmonary consolidation",
                "confidence": 0.85
            })
            
            if patient_age > 60:
                critical_findings.append("Elderly patient with respiratory symptoms requires immediate attention")
                recommendations.append("Consider immediate oxygen therapy")
                
            recommendations.append("Schedule follow-up chest X-ray in 24-48 hours")
            
        if "fever" in symptoms.lower() or "fever" in clinical_notes.lower() if clinical_notes else "":
            findings.append({
                "region": "systemic",
                "finding": "Febrile state detected",
                "confidence": 0.92
            })
            recommendations.append("Monitor temperature every 4 hours")
            
        # Generate explanation using clinical reasoning
        explanation = self._generate_clinical_explanation(
            findings, patient_age, patient_gender, symptoms
        )
        
        return {
            "findings": findings,
            "recommendations": recommendations,
            "critical_findings": critical_findings,
            "explanation": explanation,
            "raw_analysis": {
                "model": "LLaVA-Med (simulated)",
                "processing_time": "1.2s"
            }
        }
    
    def _generate_clinical_explanation(self, findings: List[Dict], 
                                      age: int, gender: str, 
                                      symptoms: str) -> str:
        """Generate natural language explanation of findings"""
        explanation_parts = [
            f"Patient is a {age}-year-old {gender.lower()} presenting with {symptoms}."
        ]
        
        for finding in findings:
            explanation_parts.append(
                f"Analysis shows {finding['finding'].lower()} in the {finding['region']} "
                f"with {finding['confidence']*100:.0f}% confidence."
            )
            
        explanation_parts.append(
            "This preliminary analysis suggests potential respiratory pathology. "
            "Clinical correlation is strongly recommended."
        )
        
        return " ".join(explanation_parts)