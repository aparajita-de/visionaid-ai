"""
VisionAid AI - Working Version    conda activate visionaid
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import uuid
from typing import Optional, List, Dict, Any
import io
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VisionAid AI", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clinical knowledge base
CLINICAL_DATA = {
    "pneumonia": {
        "keywords": ["cough", "fever", "chest pain", "shortness"],
        "icd10": "J18.9",
        "cpt": "71045",
        "severity": "urgent",
        "recommendations": [
            "Chest X-ray recommended",
            "Monitor oxygen saturation",
            "Consider antibiotics",
            "Follow up in 24-48 hours"
        ]
    },
    "tuberculosis": {
        "keywords": ["chronic cough", "weight loss", "night sweats", "blood", "coughing blood"],
        "icd10": "A15.0",
        "cpt": "71250",
        "severity": "critical",
        "recommendations": [
            "Immediate TB testing required",
            "Isolation precautions",
            "Contact tracing needed"
        ]
    },
    "fracture": {
        "keywords": ["pain", "swelling", "deformity", "injury"],
        "icd10": "S32.9",
        "cpt": "73090",
        "severity": "urgent",
        "recommendations": [
            "Immobilize affected area",
            "X-ray for confirmation",
            "Orthopedic consultation"
        ]
    },
    "normal": {
        "keywords": ["clear", "normal", "no symptoms", "routine"],
        "icd10": "Z01.89",
        "cpt": "99212",
        "severity": "non_urgent",
        "recommendations": [
            "Routine follow-up",
            "Continue current management",
            "Return if symptoms develop"
        ]
    }
}

# Store audit logs
audit_logs = {}

@app.get("/")
async def root():
    return {
        "message": "VisionAid AI API",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/diagnose")
async def diagnose(
    file: UploadFile = File(...),
    patient_age: int = Form(...),
    patient_gender: str = Form(...),
    symptoms: str = Form(...),
    clinical_notes: Optional[str] = Form(None)
):
    """Main diagnosis endpoint"""
    session_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        logger.info(f"Processing session: {session_id}")
        
        # Validate inputs
        if patient_age < 0 or patient_age > 120:
            raise HTTPException(status_code=400, detail="Invalid age")
        
        if patient_gender not in ["male", "female", "other"]:
            raise HTTPException(status_code=400, detail="Invalid gender")
        
        # Validate file
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Please upload JPEG or PNG images")
        
        # Read and validate image
        image_bytes = await file.read()
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()
            logger.info(f"Image validated: {img.format}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")
        
        # Analyze symptoms
        analysis = analyze_symptoms(symptoms, patient_age, clinical_notes)
        
        # Prepare response
        response = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "preliminary_diagnosis": analysis["findings"],
            "confidence_score": analysis["confidence"],
            "icd10_codes": analysis["icd10_codes"],
            "cpt_codes": analysis["cpt_codes"],
            "recommendations": analysis["recommendations"],
            "critical_findings": analysis["critical_findings"],
            "explanation": analysis["explanation"],
            "severity": analysis["severity"],
            "audit_id": session_id
        }
        
        # Store audit log
        audit_logs[session_id] = {
            "session_id": session_id,
            "timestamp": start_time.isoformat(),
            "patient_age": patient_age,
            "patient_gender": patient_gender,
            "symptoms": symptoms,
            "analysis": analysis,
            "processing_time": (datetime.now() - start_time).total_seconds()
        }
        
        logger.info(f"Analysis complete for {session_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in session {session_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/audit/{session_id}")
async def get_audit_log(session_id: str):
    """Retrieve audit log"""
    log = audit_logs.get(session_id)
    if not log:
        raise HTTPException(status_code=404, detail="Session not found")
    return log

def analyze_symptoms(symptoms: str, age: int, notes: Optional[str]) -> Dict[str, Any]:
    """Analyze symptoms and generate findings"""
    all_text = f"{symptoms} {notes or ''}".lower()
    
    findings = []
    recommendations = []
    critical_findings = []
    icd10_codes = []
    cpt_codes = []
    severity = "non_urgent"
    
    # Match conditions
    for condition, data in CLINICAL_DATA.items():
        if any(keyword in all_text for keyword in data["keywords"]):
            findings.append({
                "region": get_region(condition),
                "finding": f"Possible {condition}",
                "confidence": 0.85,
                "icd10_code": data["icd10"]
            })
            recommendations.extend(data["recommendations"])
            icd10_codes.append(data["icd10"])
            cpt_codes.append(data["cpt"])
            
            if data["severity"] == "critical":
                critical_findings.append(f"⚠️ CRITICAL: {condition} suspected")
                severity = "critical"
            elif data["severity"] == "urgent" and severity != "critical":
                severity = "urgent"
                critical_findings.append(f"⚠️ {condition} requires prompt evaluation")
    
    # Age considerations
    if age > 65:
        critical_findings.append("👴 Elderly patient requires careful monitoring")
        if severity == "non_urgent":
            severity = "urgent"
    
    # Default if no matches
    if not findings:
        findings.append({
            "region": "general",
            "finding": "No specific findings identified",
            "confidence": 0.70,
            "icd10_code": "R69"
        })
        recommendations.append("Continue monitoring symptoms")
        icd10_codes.append("R69")
    
    # Always add consultation code
    if "99243" not in cpt_codes:
        cpt_codes.append("99243")
    
    # Remove duplicates
    icd10_codes = list(dict.fromkeys(icd10_codes))
    cpt_codes = list(dict.fromkeys(cpt_codes))
    recommendations = list(dict.fromkeys(recommendations))[:5]
    
    # Generate explanation
    explanation = f"Patient is {age} years old. "
    explanation += f"Symptoms: {symptoms}. "
    explanation += f"Analysis suggests {findings[0]['finding'].lower()} with {findings[0]['confidence']*100:.0f}% confidence. "
    
    if severity == "critical":
        explanation += "⚠️ This case requires immediate attention and specialist consultation. "
    elif severity == "urgent":
        explanation += "⚠️ This case requires prompt evaluation. "
    else:
        explanation += "This case appears stable but requires clinical correlation. "
    
    explanation += "All findings must be verified by a qualified healthcare professional."
    
    return {
        "findings": findings,
        "recommendations": recommendations,
        "critical_findings": critical_findings,
        "explanation": explanation,
        "severity": severity,
        "confidence": findings[0]["confidence"],
        "icd10_codes": icd10_codes,
        "cpt_codes": cpt_codes
    }

def get_region(condition: str) -> str:
    """Map condition to body region"""
    regions = {
        "pneumonia": "lungs",
        "tuberculosis": "lungs",
        "fracture": "bone",
        "normal": "general"
    }
    return regions.get(condition, "affected area")

# This is the key fix - don't use reload=True when running directly
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 VisionAid AI Server Starting...")
    print("="*50)
    print(f"📍 Server: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🔍 Health: http://localhost:8000/api/health")
    print("="*50 + "\n")
    # Remove reload=True to fix the issue
    uvicorn.run(app, host="127.0.0.1", port=8000)