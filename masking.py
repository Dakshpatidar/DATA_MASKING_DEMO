
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_lg")


def mask_sensitive_data(text: str):

    doc = nlp(text)

    masked_text = text

    mapping = {}

    audit_table = []

    counters = {
        "PERSON": 1,
        "ORG": 1,
        "GPE": 1
    }

    entity_map = {
        "PERSON": "NAME",
        "ORG": "ORG",
        "GPE": "LOCATION"
    }

    # Sort entities by length
    entities = sorted(
        doc.ents,
        key=lambda x: len(x.text),
        reverse=True
    )

    for ent in entities:

        # =========================
        # SKIP REGEX TOKENS
        # =========================

        if "ZX" in ent.text:
            continue

        # =========================
        # IGNORE SMALL / NOISY TOKENS
        # =========================

        if len(ent.text.strip()) <= 3:
            continue

        # =========================
        # IGNORE COMMON FALSE POSITIVES
        # =========================

        blocked_words = {
            "email",
            "phone",
            "number",
            "address",
            "contact"
        }

        if ent.text.lower() in blocked_words:
            continue

        # =========================
        # PROCESS VALID ENTITIES
        # =========================

        if ent.label_ in entity_map:

            entity_type = entity_map[ent.label_]

            token = f"[{entity_type}_{counters[ent.label_]}]"

            masked_text = masked_text.replace(
                ent.text,
                token
            )

            mapping[token] = ent.text

            audit_table.append({
                "type": entity_type,
                "original": ent.text,
                "masked": token,
                "method": "NER"
            })

            counters[ent.label_] += 1

    return masked_text, mapping, audit_table


def unmask_text(text: str, mapping: dict):

    for token, original_value in mapping.items():

        text = text.replace(
            token,
            original_value
        )

    return text
