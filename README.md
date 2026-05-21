# 🛡 Secure AI Privacy Gateway

A privacy-first AI system that protects sensitive user information before sending prompts to Large Language Models (LLMs).

The main goal of this project is to create a secure AI layer where users can interact with AI systems without directly exposing confidential data to the model.

---

# 🚀 What This Project Does

This project currently provides two main features:

## 1. Data Masking Service

Users can paste sensitive text and the system automatically masks confidential information before sharing or processing it.

### Supported Sensitive Entities

* Email Addresses
* Phone Numbers
* PAN Numbers
* Aadhaar Numbers
* Person Names
* Organizations
* Locations

### Privacy Architecture Used

The project uses a Hybrid Privacy Pipeline:

* **Regex-based masking** for structured entities
  (Email, Phone, PAN, Aadhaar)

* **NER-based masking using spaCy** for contextual entities
  (Names, Organizations, Locations)

This hybrid approach improves overall masking coverage and accuracy.

---

## 2. Secure AI Assistant

A privacy-safe AI chatbot where sensitive user data is automatically masked before reaching the LLM.

### Flow

1. User sends prompt
2. Sensitive information gets masked
3. Masked prompt is sent to the LLM
4. LLM generates response securely
5. Original values are restored safely

This ensures that raw sensitive user data never directly reaches the AI model.

---

# 🔍 Transparency Panel

The project also includes a transparency panel that shows:

* what data was masked
* masking method used
* generated placeholder tokens

This helps improve:

* explainability
* transparency
* user trust

---

# 📊 Benchmarking & Evaluation

The project also includes a small evaluation pipeline to benchmark:

* Precision
* Recall
* F1 Score
* Latency

using manually created sensitive-entity test cases.

Run evaluation:

```bash
python evaluation.py
```

---

# ⚙ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI

### NLP / AI

* spaCy
* Groq API

### Privacy Layer

* Regex + NER Hybrid Masking

---

# 🚀 How to Run the Project

## 1. Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install spaCy Model

```bash
python -m spacy download en_core_web_lg
```

---

## 4. Add API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

---

# ▶ Run Backend

```bash
python -m uvicorn main:app --reload
```

---

# ▶ Run Frontend

Open a new terminal and run:

```bash
streamlit run app.py
```

---
for evaluation metrics run in new terminal 
python evaluation.py

# 📂 Main Project Files

* `app.py` → Streamlit frontend
* `main.py` → FastAPI backend
* `masking.py` → NER masking logic
* `regex_masking.py` → Regex masking logic
* `llm_service.py` → Groq LLM integration
* `evaluation.py` → Benchmarking & evaluation pipeline

---
