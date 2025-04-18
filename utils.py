import re

# Strict patterns for PII/PCI
PII_PATTERNS = {
    "full_name":  r'\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)?\s*[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b',
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b",
    "phone_number": r"\+?\d{1,4}[-\s]?\(?\d{1,4}\)?[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{1,4}",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",  # 12/25/1990
    "aadhar_num": r"\b\d{12}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    # expiry only MM/YY, not DOB
    "expiry_no": r"\b(0[1-9]|1[0-2])[/-]\d{2}\b",
}


def mask_pii_entities(text: str) -> dict:
    """
    Detects and masks PII/PCI fields in `text`, returning:
      {
        "masked_email": "...",
        "masked_entities": [
           {"position":[s,e], "classification":"dob", "entity":"12/25/1990"}, ...
        ]
      }
    Overlapping matches are resolved in favor of the longest match first.
    """
    # 1) Gather all regex matches
    raw_matches = []
    for label, pattern in PII_PATTERNS.items():
        for m in re.finditer(pattern, text):
            raw_matches.append(
                {
                    "classification": label,
                    "entity": m.group(),
                    "position": [m.start(), m.end()],
                    "length": m.end() - m.start(),
                }
            )

    # 2) Sort by descending match length (so dob > expiry_no)
    raw_matches.sort(key=lambda x: x["length"], reverse=True)

    # 3) Filter out overlaps
    used_positions = set()
    final_matches = []
    for m in raw_matches:
        s, e = m["position"]
        if not any(pos in used_positions for pos in range(s, e)):
            final_matches.append(m)
            used_positions.update(range(s, e))

    # 4) Mask in one pass (from left to right), adjusting offsets
    masked = text
    offset = 0
    for m in sorted(final_matches, key=lambda x: x["position"][0]):
        s, e = m["position"]
        tag = f"[{m['classification']}]"
        masked = masked[: s + offset] + tag + masked[e + offset :]
        offset += len(tag) - (e - s)

    # 5) Build masked_entities list (drop the internal 'length' key)
    masked_entities = [
        {
            "position": m["position"],
            "classification": m["classification"],
            "entity": m["entity"],
        }
        for m in final_matches
    ]

    return {"masked_email": masked, "masked_entities": masked_entities}