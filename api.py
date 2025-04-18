from flask import Blueprint, jsonify, request

from models import classify_email_category, classify_email_model
from utils import mask_pii_entities

# This name must match what app.py imports
classify_email_route = Blueprint("classify_email", __name__)


@classify_email_route.route("/classify_email", methods=["POST"])
def classify_email():
    data = request.get_json() or {}
    email_body = data.get("email")

    if not isinstance(email_body, str) or not email_body.strip():
        return jsonify({"error": "Missing or invalid 'email' field"}), 400

    # 1. Mask PII
    masked = mask_pii_entities(email_body)

    # 2. Classify (ML model with fallback)
    category = classify_email_model(masked["masked_email"])
    # (classify_email_model returns fallback if model not found)

    # 3. Build response
    return (
        jsonify(
            {
                "input_email_body": email_body,
                "list_of_masked_entities": masked["masked_entities"],
                "masked_email": masked["masked_email"],
                "category_of_the_email": category,
            }
        ),
        200,
    )