from fastapi import FastAPI
from pydantic import BaseModel

from masking import mask_sensitive_data, unmask_text
from regex_masking import regex_mask_sensitive_data
from llm_service import get_llm_response

app = FastAPI()


# =====================================================
# REQUEST MODEL
# =====================================================

class UserRequest(BaseModel):
    text: str


# =====================================================
# DISPLAY TOKEN FORMAT
# =====================================================

def make_display_text(text):

    if text is None:
        return ""

    text = text.replace("__EMAIL_", "[EMAIL_")
    text = text.replace("__PHONE_", "[PHONE_")
    text = text.replace("__PAN_", "[PAN_")
    text = text.replace("__AADHAAR_", "[AADHAAR_")

    text = text.replace("__", "]")

    return text


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Secure AI Privacy Gateway Running"
    }


# =====================================================
# DATA MASKING SERVICE
# =====================================================

@app.post("/hybrid-mask-and-send")
def hybrid_mask_and_send(request: UserRequest):

    regex_masked_text, regex_mapping, regex_audit = (
        regex_mask_sensitive_data(request.text)
    )

    ner_masked_text, ner_mapping, ner_audit = (
        mask_sensitive_data(regex_masked_text)
    )

    combined_mapping = {
        **regex_mapping,
        **ner_mapping
    }

    combined_audit = regex_audit + ner_audit

    return {

        "original_text": request.text,

        "masked_text": make_display_text(
            ner_masked_text
        ),

        "masked_entities": combined_audit,

        "mapping": combined_mapping
    }


# =====================================================
# SECURE AI ASSISTANT
# =====================================================

@app.post("/secure-ai-chat")
def secure_ai_chat(request: UserRequest):

    try:

        # =========================
        # REGEX MASKING
        # =========================

        regex_masked_text, regex_mapping, regex_audit = (
            regex_mask_sensitive_data(request.text)
        )

        # =========================
        # NER MASKING
        # =========================

        ner_masked_text, ner_mapping, ner_audit = (
            mask_sensitive_data(regex_masked_text)
        )

        combined_mapping = {
            **regex_mapping,
            **ner_mapping
        }

        combined_audit = regex_audit + ner_audit

        display_masked_prompt = make_display_text(
            ner_masked_text
        )

        print("\n========================")
        print("MASKED PROMPT")
        print(display_masked_prompt)
        print("========================\n")

        # =========================
        # SEND TO LLM
        # =========================

        llm_response = get_llm_response(
            display_masked_prompt
        )

        # =========================
        # UNMASK RESPONSE
        # =========================

        final_response = unmask_text(
            llm_response,
            combined_mapping
        )

        return {

            "retrieved_context": "No document uploaded yet.",

            "masked_prompt": display_masked_prompt,

            "masked_entities": combined_audit,

            "final_response": final_response
        }

    except Exception as e:

        print("\n========================")
        print("BACKEND ERROR")
        print(str(e))
        print("========================\n")

        return {

            "retrieved_context": "",

            "masked_prompt": "",

            "masked_entities": [],

            "final_response": f"Backend Error: {str(e)}"
        }