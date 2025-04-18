import re

import spacy

nlp = spacy.load("en_core_web_sm")

ENTITY_PATTERNS = {
    "aadhar": r"\b\d{12}\b",
    "dob": r"\b\d{2}/\d{2}/\d{4}\b",
    "expiry_no": r"\b\d{2}/\d{2}\b",
    "cvv": r"\b\d{3}\b",
    "phone": r"\+?\d{1,4}[-\s]?\(?\d{1,4}\)?[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{1,4}",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z|a-z]{2,}\b",
}


def extract_entities(text):
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    entities_raw = []

    # Collect all matches first (don't filter overlaps yet)
    for label, pattern in ENTITY_PATTERNS.items():
        for m in re.finditer(pattern, text):
            entities_raw.append(
                {
                    "classification": label,
                    "entity": m.group(),
                    "position": [m.start(), m.end()],
                }
            )

    # Sort by length (desc) so longer matches like dob come before expiry_no
    entities_raw.sort(key=lambda x: x["position"][1] - x["position"][0], reverse=True)

    used_positions = set()
    final_entities = []

    for ent in entities_raw:
        s, e = ent["position"]
        # Only add if this span is not overlapping with already used characters
        if not any(i in used_positions for i in range(s, e)):
            final_entities.append(ent)
            used_positions.update(range(s, e))

    # Add spaCy NER for person names
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not any(
            i in used_positions for i in range(ent.start_char, ent.end_char)
        ):
            final_entities.append(
                {
                    "classification": "persons_name",
                    "entity": ent.text,
                    "position": [ent.start_char, ent.end_char],
                }
            )
            used_positions.update(range(ent.start_char, ent.end_char))

    return sorted(final_entities, key=lambda x: x["position"][0])


def mask_text(text, entities):
    masked = text
    offset = 0
    for ent in sorted(entities, key=lambda x: x["position"][0]):
        s, e = ent["position"]
        tag = f"[{ent['classification']}]"
        masked = masked[: s + offset] + tag + masked[e + offset :]
        offset += len(tag) - (e - s)

    return masked