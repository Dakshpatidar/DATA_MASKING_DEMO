# LLM-Based Privacy Masking Gateway

A hybrid privacy-preserving AI gateway that masks sensitive user information before sending data to an LLM.

The system combines:

- Regex-based masking for structured sensitive data
- spaCy Named Entity Recognition (NER) for contextual entities
- LLM integration using Groq API
- Secure unmasking pipeline
- Latency monitoring system

---

# Features

## Regex-Based Sensitive Data Detection

Masks:

- Email
- Phone Number
- PAN Number
- Aadhaar Number

Example:

```text
rahul@gmail.com → [EMAIL_1]
9876543210 → [PHONE_1]
```

---

## NER-Based Entity Detection

Using spaCy NER model:

- PERSON
- ORGANIZATION
- LOCATION

Example:

```text
Rahul Sharma → [NAME_1]
Infosys → [ORG_1]
Delhi → [LOCATION_1]
```

---

## Hybrid Privacy Pipeline

Flow:

```text
User Input
   ↓
Regex Masking
   ↓
NER Masking
   ↓
LLM Request
   ↓
LLM Response
   ↓
Unmasking
   ↓
Final Secure Response
```

---

# Tech Stack

- Python
- FastAPI
- spaCy
- Regex
- Groq API
- Uvicorn
- Pydantic

---

# Architecture

```text
Client
  ↓
FastAPI Gateway
  ↓
Regex Masking Layer
  ↓
NER Masking Layer
  ↓
LLM (Groq)
  ↓
Response Unmasking
  ↓
Secure Response
```

---

# API Endpoints

## NER Endpoint

```http
POST /mask-and-send
```

Uses only spaCy NER masking.

---

## Hybrid Endpoint

```http
POST /hybrid-mask-and-send
```

Uses:

- Regex masking
- NER masking
- LLM processing
- Secure unmasking

---

# Example Request

```json
{
  "text": "Rahul Sharma works at Infosys. Email is rahul@gmail.com and phone is 9876543210"
}
```

---

# Example Response

```json
{
  "masked_text": "[NAME_1] works at [ORG_1]. Email is [EMAIL_1] and phone is [PHONE_1]"
}
```

---

# Latency Metrics

The system measures:

- Regex masking latency
- NER masking latency
- LLM response latency
- Unmasking latency
- Total processing latency

---

# Installation

## Clone Repository

```bash
git clone <your-github-link>
cd Data-Masking
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Environment

### Mac/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Download spaCy Model

```bash
python -m spacy download en_core_web_lg
```

---

# Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

---

# Run Locally

```bash
uvicorn main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

