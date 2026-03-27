from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any

class DiagnosisRequest(BaseModel):
    """Request model for diagnosis"""
    patient_age: int
    patient_gender: str
    symptoms: str
    clinical_notes: Optional[str] = None

class Finding(BaseModel):
    """Finding model"""
    region: str
    finding: str
    confidence: float
    icd10_code: Optional[str] = None

class DiagnosisResponse(BaseModel):
    """Response model for diagnosis"""
    session_id: str
    timestamp: datetime
    preliminary_diagnosis: List[Finding]
    confidence_score: float
    icd10_codes: List[str]
    cpt_codes: List[str]
    recommendations: List[str]
    critical_findings: List[str]
    explanation: str
    audit_id: str

class AuditLog(BaseModel):
    """Audit log model"""
    id: str
    session_id: str
    timestamp: datetime
    patient_age: int
    patient_gender: str
    symptoms: str
    diagnosis: Dict[str, Any]
    guardrail_validation: Dict[str, Any]
    compliance_codes: Dict[str, Any]
    processing_time: float
    error: Optional[str] = None