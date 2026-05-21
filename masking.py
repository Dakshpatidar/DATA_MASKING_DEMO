import spacy
import re


# =====================================================
# LOAD SPACY MODEL
# =====================================================

nlp = spacy.load("en_core_web_lg")


# =====================================================
# MASK SENSITIVE DATA
# =====================================================

def mask_sensitive_data(text: str):

    masked_text = text

    mapping = {}

    audit_table = []

    # =====================================================
    # COUNTERS
    # =====================================================

    counters = {
        "NAME": 1,
        "ORG": 1,
        "LOCATION": 1
    }

    # =====================================================
    # CUSTOM NAME PATTERNS
    # =====================================================

    custom_name_patterns = [

        r"my name is ([a-zA-Z]+\s[a-zA-Z]+)",

        r"i am ([a-zA-Z]+\s[a-zA-Z]+)",

        r"this is ([a-zA-Z]+\s[a-zA-Z]+)"
    ]

    # =====================================================
    # CUSTOM NAME MASKING
    # =====================================================

    for pattern in custom_name_patterns:

        matches = re.finditer(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:

            detected_name = match.group(1)

            # SKIP DUPLICATES
            if detected_name in mapping.values():
                continue

            token = f"[NAME_{counters['NAME']}]"

            masked_text = masked_text.replace(
                detected_name,
                token
            )

            mapping[token] = detected_name

            audit_table.append({

                "type": "NAME",

                "original": detected_name,

                "masked": token,

                "method": "CUSTOM_REGEX"
            })

            counters["NAME"] += 1

    # =====================================================
    # SPACY NER
    # =====================================================

    doc = nlp(text)

    entities = sorted(
        doc.ents,
        key=lambda x: len(x.text),
        reverse=True
    )

    # =====================================================
    # ENTITY MAP
    # =====================================================

    entity_map = {

        "PERSON": "NAME",

        "ORG": "ORG",

        "GPE": "LOCATION"
    }

    # =====================================================
    # IGNORE WORDS
    # =====================================================

    ignore_words = [

        "ai",

        "ml",

        "llm",

        "nlp",

        "python",

        "chatgpt",

        "openai"
    ]

    # =====================================================
    # PROCESS ENTITIES
    # =====================================================

    for ent in entities:

        entity_text = ent.text.strip()

        # =====================================================
        # SKIP EMPTY
        # =====================================================

        if not entity_text:
            continue

        # =====================================================
        # SKIP MASKED TOKENS
        # =====================================================

        if "[" in entity_text and "]" in entity_text:
            continue

        # =====================================================
        # SKIP DUPLICATES
        # =====================================================

        if entity_text in mapping.values():
            continue

        # =====================================================
        # IGNORE TECH WORDS
        # =====================================================

        if entity_text.lower() in ignore_words:
            continue

        # =====================================================
        # VALID ENTITY
        # =====================================================

        if ent.label_ in entity_map:

            entity_type = entity_map[ent.label_]

            token = f"[{entity_type}_{counters[entity_type]}]"

            masked_text = masked_text.replace(
                entity_text,
                token
            )

            mapping[token] = entity_text

            audit_table.append({

                "type": entity_type,

                "original": entity_text,

                "masked": token,

                "method": "NER"
            })

            counters[entity_type] += 1

    # =====================================================
    # RETURN
    # =====================================================

    return masked_text, mapping, audit_table


# =====================================================
# UNMASK TEXT
# =====================================================

def unmask_text(text: str, mapping: dict):

    for token, original_value in mapping.items():

        text = text.replace(
            token,
            original_value
        )

    return text