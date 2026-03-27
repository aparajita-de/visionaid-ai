// Configuration
const API_URL = 'http://localhost:8000';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const auditSection = document.getElementById('auditSection');

let selectedFile = null;

// Event Listeners
if (uploadArea) uploadArea.addEventListener('click', () => fileInput.click());
if (selectFileBtn) selectFileBtn.addEventListener('click', () => fileInput.click());
if (fileInput) fileInput.addEventListener('change', handleFileSelect);
if (analyzeBtn) analyzeBtn.addEventListener('click', handleAnalyze);

// Drag and drop
if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = '#f8f9ff';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.background = 'transparent';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.background = 'transparent';
        
        const file = e.dataTransfer.files[0];
        if (file && (file.type.startsWith('image/') || file.name.match(/\.(jpg|jpeg|png)$/i))) {
            selectedFile = file;
            updateFilePreview(file);
            if (analyzeBtn) analyzeBtn.disabled = false;
        } else {
            showError('Please upload a valid medical image (JPEG, PNG)');
        }
    });
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        selectedFile = file;
        updateFilePreview(file);
        if (analyzeBtn) analyzeBtn.disabled = false;
    }
}

function updateFilePreview(file) {
    if (!uploadArea) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadArea.innerHTML = `
            <div class="upload-icon">✅</div>
            <p>File selected: ${file.name}</p>
            <p class="file-info">${(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <button class="btn-secondary" onclick="changeFile()">Change File</button>
        `;
    };
    reader.readAsDataURL(file);
}

window.changeFile = function() {
    selectedFile = null;
    if (analyzeBtn) analyzeBtn.disabled = true;
    if (fileInput) fileInput.value = '';
    if (uploadArea) {
        uploadArea.innerHTML = `
            <div class="upload-icon">📷</div>
            <p>Drag & drop medical images here</p>
            <p class="file-info">Supports: DICOM, JPEG, PNG (max 50MB)</p>
            <button class="btn-secondary" id="selectFileBtn">Select File</button>
        `;
        const newSelectBtn = document.getElementById('selectFileBtn');
        if (newSelectBtn) newSelectBtn.addEventListener('click', () => fileInput.click());
    }
};

async function handleAnalyze() {
    if (!selectedFile) {
        showError('Please select a medical image first');
        return;
    }
    
    const patientAge = document.getElementById('patientAge')?.value;
    const patientGender = document.getElementById('patientGender')?.value;
    const symptoms = document.getElementById('symptoms')?.value;
    const clinicalNotes = document.getElementById('clinicalNotes')?.value;
    
    if (!patientAge || !symptoms) {
        showError('Please fill in all required fields');
        return;
    }
    
    // Show loading state
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        const btnText = analyzeBtn.querySelector('.btn-text');
        const btnLoader = analyzeBtn.querySelector('.btn-loader');
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline';
    }
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('patient_age', patientAge);
    formData.append('patient_gender', patientGender);
    formData.append('symptoms', symptoms);
    if (clinicalNotes) formData.append('clinical_notes', clinicalNotes);
    
    try {
        const response = await fetch(`${API_URL}/api/diagnose`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        const result = await response.json();
        displayResults(result);
        
        // Fetch audit log
        const auditResponse = await fetch(`${API_URL}/api/audit/${result.session_id}`);
        if (auditResponse.ok) {
            const auditLog = await auditResponse.json();
            displayAudit(auditLog);
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to analyze the image. Please try again.');
    } finally {
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            const btnText = analyzeBtn.querySelector('.btn-text');
            const btnLoader = analyzeBtn.querySelector('.btn-loader');
            if (btnText) btnText.style.display = 'inline';
            if (btnLoader) btnLoader.style.display = 'none';
        }
    }
}

function displayResults(result) {
    if (resultsSection) resultsSection.style.display = 'block';
    
    // Display confidence badge
    const confidenceBadge = document.getElementById('confidenceBadge');
    if (confidenceBadge) {
        const confidencePercent = (result.confidence_score * 100).toFixed(0);
        confidenceBadge.textContent = `Confidence: ${confidencePercent}%`;
        confidenceBadge.className = 'confidence-badge';
        if (result.confidence_score >= 0.8) {
            confidenceBadge.classList.add('confidence-high');
        } else if (result.confidence_score >= 0.6) {
            confidenceBadge.classList.add('confidence-medium');
        } else {
            confidenceBadge.classList.add('confidence-low');
        }
    }
    
    // Display critical findings
    const criticalAlert = document.getElementById('criticalAlert');
    const criticalFindings = document.getElementById('criticalFindings');
    if (criticalAlert && criticalFindings) {
        if (result.critical_findings && result.critical_findings.length > 0) {
            criticalAlert.style.display = 'flex';
            criticalFindings.textContent = result.critical_findings.join(', ');
        } else {
            criticalAlert.style.display = 'none';
        }
    }
    
    // Display findings - FIX: Remove duplicates and format properly
    const findingsList = document.getElementById('findingsList');
    if (findingsList) {
        findingsList.innerHTML = '';
        // Remove duplicates by using a Set
        const uniqueFindings = [];
        const seen = new Set();
        for (const finding of result.preliminary_diagnosis) {
            const key = `${finding.region}-${finding.finding}`;
            if (!seen.has(key)) {
                seen.add(key);
                uniqueFindings.push(finding);
            }
        }
        
        uniqueFindings.forEach(finding => {
            findingsList.innerHTML += `
                <div class="finding-item">
                    <strong>${finding.region}</strong>
                    <p>${finding.finding}</p>
                    <small>Confidence: ${(finding.confidence * 100).toFixed(0)}%</small>
                </div>
            `;
        });
    }
    
    // Display explanation
    const explanation = document.getElementById('explanation');
    if (explanation) explanation.textContent = result.explanation;
    
    // Display recommendations - FIX: Use bullet points, not X marks
    const recommendationsList = document.getElementById('recommendations');
    if (recommendationsList) {
        recommendationsList.innerHTML = '';
        result.recommendations.forEach(rec => {
            recommendationsList.innerHTML += `<li>✓ ${rec}</li>`;
        });
    }
    
    // Display codes - FIX: Remove duplicates
    const icd10Container = document.getElementById('icd10Codes');
    const cptContainer = document.getElementById('cptCodes');
    
    if (icd10Container) {
        // Remove duplicates using Set
        const uniqueIcd10 = [...new Set(result.icd10_codes)];
        icd10Container.innerHTML = uniqueIcd10.map(code => `<div>${code}</div>`).join('');
    }
    
    if (cptContainer) {
        const uniqueCpt = [...new Set(result.cpt_codes)];
        cptContainer.innerHTML = uniqueCpt.map(code => `<div>${code}</div>`).join('');
    }
    
    // Scroll to results
    if (resultsSection) resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Setup buttons
    const downloadBtn = document.getElementById('downloadReportBtn');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    
    if (downloadBtn) downloadBtn.onclick = () => downloadReport(result);
    if (newAnalysisBtn) newAnalysisBtn.onclick = () => resetAnalysis();
}

function displayAudit(auditLog) {
    if (auditSection) {
        auditSection.style.display = 'block';
        const auditInfo = document.getElementById('auditInfo');
        if (auditInfo) {
            auditInfo.innerHTML = `
                <div style="font-family: monospace; font-size: 12px;">
                    <strong>Session ID:</strong> ${auditLog.session_id}<br>
                    <strong>Timestamp:</strong> ${new Date(auditLog.timestamp).toLocaleString()}<br>
                    <strong>Processing Time:</strong> ${auditLog.processing_time?.toFixed(2) || 'N/A'} seconds<br>
                    <strong>Status:</strong> ✅ Analysis Complete
                </div>
            `;
        }
    }
}

function downloadReport(result) {
    // Remove duplicates for report
    const uniqueIcd10 = [...new Set(result.icd10_codes)];
    const uniqueCpt = [...new Set(result.cpt_codes)];
    
    const reportContent = `
VisionAid AI Preliminary Analysis Report
=========================================
Session ID: ${result.session_id}
Date: ${new Date(result.timestamp).toLocaleString()}

Confidence Score: ${(result.confidence_score * 100).toFixed(0)}%

FINDINGS:
${result.preliminary_diagnosis.map(f => `- ${f.region}: ${f.finding} (${(f.confidence * 100).toFixed(0)}% confidence)`).join('\n')}

CLINICAL EXPLANATION:
${result.explanation}

RECOMMENDATIONS:
${result.recommendations.map(r => `- ${r}`).join('\n')}

COMPLIANCE CODES:
ICD-10: ${uniqueIcd10.join(', ')}
CPT: ${uniqueCpt.join(', ')}

${result.critical_findings.length > 0 ? '⚠️ CRITICAL FINDINGS: ' + result.critical_findings.join(', ') : ''}

DISCLAIMER: This is an AI-assisted preliminary analysis. All findings require clinical correlation and verification by a qualified healthcare professional.
    `;
    
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `visionaid_report_${result.session_id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

function resetAnalysis() {
    if (resultsSection) resultsSection.style.display = 'none';
    if (auditSection) auditSection.style.display = 'none';
    selectedFile = null;
    if (fileInput) fileInput.value = '';
    
    const ageInput = document.getElementById('patientAge');
    const symptomsInput = document.getElementById('symptoms');
    const notesInput = document.getElementById('clinicalNotes');
    
    if (ageInput) ageInput.value = '';
    if (symptomsInput) symptomsInput.value = '';
    if (notesInput) notesInput.value = '';
    
    if (uploadArea) {
        uploadArea.innerHTML = `
            <div class="upload-icon">📷</div>
            <p>Drag & drop medical images here</p>
            <p class="file-info">Supports: DICOM, JPEG, PNG (max 50MB)</p>
            <button class="btn-secondary" id="selectFileBtn">Select File</button>
        `;
        const newSelectBtn = document.getElementById('selectFileBtn');
        if (newSelectBtn) newSelectBtn.addEventListener('click', () => fileInput.click());
    }
    
    if (analyzeBtn) analyzeBtn.disabled = true;
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f8d7da;
        color: #721c24;
        padding: 12px 20px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

// Add slide-in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);