# VisionAid AI - GenAI-Powered Diagnostic Support for Rural Healthcare



**VisionAid AI** bridges the critical gap in rural healthcare by transforming medical imaging data into natural language, specialist-level diagnostic insights[span_0](start_span)[span_0](end_span). Designed for areas with adequate equipment but a shortage of on-site radiologists, this platform empowers General Practitioners (GPs) to make rapid, informed decisions[span_1](start_span)[span_1](end_span).

For detailed development history and original competitive proposals, please refer to the project documentation file: `Aparajita De_ET Gen AI Hackathon.pdf`.

---

## 👥 Team Information
* **Team Name:** rupkotha4002[span_2](start_span)[span_2](end_span)
* **Team Member:** Aparajita De (Solo)[span_3](start_span)[span_3](end_span)
* **College:** College of Engineering & Management, Kolaghat[span_4](start_span)[span_4](end_span)

---

## 📌 Problem Statement
Rural healthcare centers often possess essential diagnostic hardware (such as X-ray and CT machines) but lack on-site specialized radiologists[span_5](start_span)[span_5](end_span). 

* **The Bottleneck:** Patients routinely wait days for a formal report[span_6](start_span)[span_6](end_span).
* **The Consequence:** Delays in life-saving treatments for critical, time-sensitive conditions like pneumonia, tuberculosis (TB), or acute fractures[span_7](start_span)[span_7](end_span).
* **Impact:** Millions of rural patients and severely overburdened General Practitioners (GPs)[span_8](start_span)[span_8](end_span).

## 💡 Motivation
The core limitation in rural medicine isn't the equipment—it is the local access to expertise[span_9](start_span)[span_9](end_span). Traditional AI tools can label an image with a binary diagnosis, but they function as a "black box[span_10](start_span)"[span_10](end_span). 

**VisionAid AI** leverages Generative AI to "explain" the pathology in structured natural language[span_11](start_span)[span_11](end_span). By helping a GP understand the underlying *why* behind a diagnosis, it democratizes specialist-level insights right at the point of care[span_12](start_span)[span_12](end_span).

## 🚀 Application & Target Users
VisionAid AI features a lightweight, accessible web-based interface built for low-bandwidth environments[span_13](start_span)[span_13](end_span).
* **Workflow:** Medical staff upload diagnostic scans $\rightarrow$ System generates an immediate **Preliminary AI Analysis Report** $\rightarrow$ High-risk cases are flagged for urgent human review[span_14](start_span)[span_14](end_span).
* **Target Users:** Rural clinics, Non-Governmental Organizations (NGOs), and Primary Health Centres (PHCs)[span_15](start_span)[span_15](end_span).

---

## 🛠️ Proposed Method
The architecture implements a sophisticated **Multimodal RAG (Retrieval-Augmented Generation)** framework[span_16](start_span)[span_16](end_span):

[ Medical Scan ] + [ Patient Vitals ]
│
▼
┌────────────────────────────────────────┐
│  Vision-Language Model (LLaVA-Med)    │
└───────────────┬────────────────────────┘
│
▼
┌────────────────────────────────────────┐
│  Clinical Contextual Layer & RAG       │
└───────────────┬────────────────────────┘
│
▼
┌────────────────────────────────────────┐
│  Safety Guardrails (Hallucination Chk) │ <─── Gold-Standard Databases
└───────────────┬────────────────────────┘
│
▼
[ Preliminary Diagnostic Report ]



1. **Vision-Language Model:** Utilizes fine-tuned medical vision-language models (e.g., LLaVA-Med or Med-PaLM 2) to interpret visual pixels directly into structured medical text[span_17](start_span)[span_17](end_span).
2. **Contextual Layer:** Integrates clinical patient vitals alongside the image data, ensuring the model evaluates the scan with proper clinical context[span_18](start_span)[span_18](end_span).
3. **Safety Guardrails:** Features a dedicated "Hallucination Check" layer that cross-references the AI's generated output against verified, gold-standard medical databases before display[span_19](start_span)[span_19](end_span).

---

## 📊 Datasets & Data Sources
The system is trained and fine-tuned using extensive, high-quality, anonymized medical datasets[span_20](start_span)[span_20](end_span):
* **Primary Sources:** NIH Chest X-ray 14, MIMIC-CXR, and Open-i (Open Access Biomedical Image Search)[span_21](start_span)[span_21](end_span).
* **Data Type:** Anonymized DICOM/JPEG images accompanied by original physician reports for robust supervised fine-tuning[span_22](start_span)[span_22](end_span).

---

## 🧪 Experiments & Validation Metrics
To guarantee clinical safety and technical viability, the project is benchmarked against three core pillars[span_23](start_span)[span_23](end_span):

| Metric Category | Evaluation Method | Target / Benchmark |
| :--- | :--- | :--- |
| **Clinical Accuracy** | F1-score and AUC-ROC evaluation[span_24](start_span)[span_24](end_span) | Tested against 1,000+ expert-annotated scans[span_25](start_span)[span_25](end_span) |
| **Expert Agreement** | Blind tests comparing AI output with human reports[span_26](start_span)[span_26](end_span) | High correlation with certified radiologist text[span_27](start_span)[span_27](end_span) |
| **Latency** | End-to-end inference timing[span_28](start_span)[span_28](end_span) | **< 15 seconds** on standard cloud GPUs for real-time utility[span_29](start_span)[span_29](end_span) |

---

## ✨ Novelty & Scale
### Novelty
Unlike standard AI classification models, VisionAid AI provides **interpretability**[span_30](start_span)[span_30](end_span). It visually highlights specific regions of interest on the scan and textually explains the findings, doubling as an active clinical teaching tool for local GPs[span_31](start_span)[span_31](end_span).

### Scope to Scale
* **Modular API:** The backend is decoupled and containerized, allowing it to easily plug into existing government health ecosystems (such as India's **e-Sanjeevani** portal)[span_32](start_span)[span_32](end_span).
* **Mobile Adaptability:** Architected to expand into a lightweight mobile application optimized for remote, low-bandwidth edge environments[span_33](start_span)[span_33](end_span).

---

## 📄 Author 
Aparajita De, BTech (AIML), CEMK(2024-2028) on ET GEN AI HACKATHON 

