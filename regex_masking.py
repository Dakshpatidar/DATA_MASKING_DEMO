import re


def regex_mask_sensitive_data(text: str):

    mapping = {}
    audit_table = []

    counters = {
        "EMAIL": 1,
        "PHONE": 1,
        "PAN": 1,
        "AADHAAR": 1
    }

    patterns = {

        "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',

        "PHONE": r'\b[6-9]\d{9}\b',

        "PAN": r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b',

        "AADHAAR": r'\b\d{4}\s\d{4}\s\d{4}\b'
    }

    masked_text = text

    for entity_type, pattern in patterns.items():

        matches = re.findall(pattern, masked_text, re.IGNORECASE)

        for match in matches:

            # INTERNAL SAFE TOKEN
            internal_token = f"__{entity_type}_{counters[entity_type]}__"

            # DISPLAY TOKEN
            display_token = f"[{entity_type}_{counters[entity_type]}]"

            masked_text = masked_text.replace(match, internal_token)

            mapping[internal_token] = match

            audit_table.append({
                "type": entity_type,
                "original": match,
                "masked": display_token,
                "method": "REGEX"
            })

            counters[entity_type] += 1

    return masked_text, mapping, audit_table