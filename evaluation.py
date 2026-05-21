from masking import mask_sensitive_data
from regex_masking import regex_mask_sensitive_data

import time


# =====================================================
# TEST DATASET
# =====================================================

test_cases = [

    {
        "text": "My name is Daksh Patidar and my email is daksh@gmail.com",

        "expected": ["NAME", "EMAIL"]
    },

    {
        "text": "I work at Infosys and my PAN is ABCDE1234F",

        "expected": ["ORG", "PAN"]
    },

    {
        "text": "Call me on 9876543210",

        "expected": ["PHONE"]
    },

    {
        "text": "My Aadhaar number is 1234 5678 9012",

        "expected": ["AADHAAR"]
    },

    {
        "text": "OpenAI is building AI systems",

        "expected": ["ORG"]
    }
]


# =====================================================
# METRICS COUNTERS
# =====================================================

TP = 0
FP = 0
FN = 0

total_latency = 0


# =====================================================
# RUN EVALUATION
# =====================================================

for case in test_cases:

    text = case["text"]

    expected = case["expected"]

    # =============================================
    # START TIMER
    # =============================================

    start = time.time()

    # =============================================
    # REGEX MASKING
    # =============================================

    regex_masked, _, regex_audit = (
        regex_mask_sensitive_data(text)
    )

    # =============================================
    # NER MASKING
    # =============================================

    ner_masked, _, ner_audit = (
        mask_sensitive_data(regex_masked)
    )

    # =============================================
    # END TIMER
    # =============================================

    latency = (
        time.time() - start
    ) * 1000

    total_latency += latency

    # =============================================
    # DETECTED ENTITIES
    # =============================================

    detected = []

    for item in regex_audit + ner_audit:

        detected.append(item["type"])

    detected = list(set(detected))

    # =============================================
    # TRUE POSITIVE
    # =============================================

    for entity in detected:

        if entity in expected:

            TP += 1

        else:

            FP += 1

    # =============================================
    # FALSE NEGATIVE
    # =============================================

    for entity in expected:

        if entity not in detected:

            FN += 1


# =====================================================
# CALCULATE METRICS
# =====================================================

precision = TP / (TP + FP) if (TP + FP) > 0 else 0

recall = TP / (TP + FN) if (TP + FN) > 0 else 0

f1_score = (
    2 * precision * recall / (precision + recall)
    if (precision + recall) > 0
    else 0
)

average_latency = total_latency / len(test_cases)


# =====================================================
# FINAL RESULTS
# =====================================================

print("\n==============================")
print("PRIVACY MASKING BENCHMARK")
print("==============================\n")

print(f"True Positives  : {TP}")
print(f"False Positives : {FP}")
print(f"False Negatives : {FN}")

print("\n==============================")

print(f"Precision : {precision:.2f}")

print(f"Recall    : {recall:.2f}")

print(f"F1 Score  : {f1_score:.2f}")

print(f"Avg Latency : {average_latency:.2f} ms")

print("\n==============================")