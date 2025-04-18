import os

import joblib

# Paths to your serialized model and vectorizer
MODEL_PATH = "models/email_classifier.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

# Load if present, else fallback to None
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    _model = joblib.load(MODEL_PATH)
    _vectorizer = joblib.load(VECTORIZER_PATH)
else:
    _model = None
    _vectorizer = None


def classify_email_category(text: str) -> str:
    """
    Simple rule-based fallback classifier.
    """
    txt = text.lower()
    if any(w in txt for w in ("refund", "buy", "order")):
        return "Purchase"
    if any(w in txt for w in ("issue", "error", "help")):
        return "Support"
    if any(w in txt for w in ("feedback", "suggestion")):
        return "Feedback"
    return "General"


def classify_email_model(text: str) -> str:
    """
    Uses ML model if loaded, else uses fallback.
    """
    if _model and _vectorizer:
        X = _vectorizer.transform([text])
        return _model.predict(X)[0]
    return classify_email_category(text)