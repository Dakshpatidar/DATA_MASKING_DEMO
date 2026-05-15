from fastapi import FastAPI
from pydantic import BaseModel

from masking import mask_sensitive_data, unmask_text
from llm_service import get_llm_response
from regex_masking import regex_mask_sensitive_data

import time

app = FastAPI()


class UserRequest(BaseModel):
    text: str


# =========================
# DISPLAY FRIENDLY TOKENS
# =========================

def make_display_text(text: str):

    text = text.replace("__EMAIL_", "[EMAIL_")
    text = text.replace("__PHONE_", "[PHONE_")
    text = text.replace("__PAN_", "[PAN_")
    text = text.replace("__AADHAAR_", "[AADHAAR_")

    text = text.replace("__", "]")

    return text


# =========================
# OLD NER ONLY ENDPOINT
# =========================

@app.post("/mask-and-send")
def mask_and_send(request: UserRequest):

    masked_text, mapping, audit_table = mask_sensitive_data(request.text)

    masked_llm_response = get_llm_response(masked_text)

    final_response = unmask_text(masked_llm_response, mapping)

    return {

        "original_text": request.text,

        "masked_text": masked_text,

        "masked_entities": audit_table,

        "mapping": mapping,

        "llm_response_masked": masked_llm_response,

        "llm_response_unmasked": final_response
    }


# =========================
# HYBRID REGEX + NER ENDPOINT
# =========================

@app.post("/hybrid-mask-and-send")
def hybrid_mask_and_send(request: UserRequest):

    total_start = time.time()

    # =========================
    # REGEX MASKING
    # =========================

    regex_start = time.time()

    regex_masked_text, regex_mapping, regex_audit = regex_mask_sensitive_data(
        request.text
    )

    regex_time = time.time() - regex_start

    # =========================
    # NER MASKING
    # =========================

    ner_start = time.time()

    ner_masked_text, ner_mapping, ner_audit = mask_sensitive_data(
        regex_masked_text
    )

    ner_time = time.time() - ner_start

    # =========================
    # COMBINED MAPPING
    # =========================

    combined_mapping = {
        **regex_mapping,
        **ner_mapping
    }

    combined_audit = regex_audit + ner_audit

    # =========================
    # LLM CALL
    # =========================

    llm_start = time.time()

    masked_llm_response = get_llm_response(
        ner_masked_text
    )

    llm_time = time.time() - llm_start

    # =========================
    # UNMASK RESPONSE
    # =========================

    unmask_start = time.time()

    final_response = unmask_text(
        masked_llm_response,
        combined_mapping
    )

    unmask_time = time.time() - unmask_start

    # =========================
    # TOTAL LATENCY
    # =========================

    total_time = time.time() - total_start

    # =========================
    # FINAL RESPONSE
    # =========================

    return {

        "original_text": request.text,

        "masked_text": make_display_text(
            ner_masked_text
        ),

        "masked_entities": combined_audit,

        "mapping": combined_mapping,

        "llm_response_masked": make_display_text(
            masked_llm_response
        ),

        "llm_response_unmasked": final_response,

        "latency_metrics": {

            "regex_time_ms": round(regex_time * 1000, 2),

            "ner_time_ms": round(ner_time * 1000, 2),

            "llm_time_ms": round(llm_time * 1000, 2),

            "unmask_time_ms": round(unmask_time * 1000, 2),

            "total_time_ms": round(total_time * 1000, 2)
        }
    }