# email_Classification_support_Sejal
The goal of this assignment is to design and implement an email classification system for a company's support team. The system should categorize incoming support emails into predefined categories while ensuring that personal information (PII) is masked before processing. After classification, the masked data should be restored to its original form.


Here's a detailed `README.md` for your email classification project, including all the necessary information, based on the files you've shared:

---

# Email Classification with PII Masking

This project implements an email classification system with **PII masking** using regex and spaCy's NER. The system is based on a machine learning model that classifies emails into different categories, such as **Purchase**, **Support**, **Feedback**, etc.

## Project Structure

- **data/emails.csv**: Dataset containing emails and their corresponding categories.
- **masking/ pii_masker.py**: Code to mask sensitive PII (Personally Identifiable Information) fields like email, phone number, Aadhar, CVV, etc.
- **models.py**: Contains the model loading, fallback classification function, and ML model logic.
- **train_model.py**: Script for training the email classification model using RandomForest and TF-IDF.
- **api.py**: Contains the API code that processes email input, applies PII masking, and classifies the email.
- **utils.py**: Contains utility functions for PII masking, including regex-based entity detection.
- **requirements.txt**: Contains all the required libraries

## Prerequisites

1. **Python 3.x**
2. **pip** (Python package manager)

## Setup

1. Clone the repository or download the project files to your local machine.
2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the **spaCy** model used for NER:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## How to Run the Project

### Step 1: Train the Model

Before running the API, you need to train the email classification model:

```bash
python train_model.py
```

This will train the model using the **emails.csv** dataset and save it in the **models** directory as `email_classifier.pkl`. The model uses **RandomForestClassifier** and **TF-IDF Vectorizer**.

### Step 2: Run the API

Once the model is trained, you can run the FastAPI server by running the following command:

```bash
python app.py
```

This will start the API on `http://localhost:5000/`.

### Step 3: Testing the API

You can test the API by sending a POST request to `http://localhost:5000/classify_email` with the following body:

```json
{
    "email": "Contact Alice Wonderland at alice@wonder.land or +91 98765 43210. DOB: 01/01/1980."
}
```

### Example Response:

```json
{
    "category_of_the_email": "General",
    "input_email_body": "Contact Alice Wonderland at alice@wonder.land or +91 98765 43210. DOB: 01/01/1980.",
    "list_of_masked_entities": [
        {
            "classification": "full_name",
            "entity": "Contact Alice Wonderland",
            "position": [
                0,
                24
            ]
        },
        {
            "classification": "email",
            "entity": "alice@wonder.land",
            "position": [
                28,
                45
            ]
        },
        {
            "classification": "phone_number",
            "entity": "+91 98765 43210",
            "position": [
                49,
                64
            ]
        },
        {
            "classification": "dob",
            "entity": "01/01/1980",
            "position": [
                71,
                81
            ]
        }
    ],
    "masked_email": "[full_name] at [email] or [phone_number]. DOB: [dob]."
}
```

## Files Overview

### **`train_model.py`**

This script trains a machine learning model using a RandomForest classifier and a TF-IDF vectorizer. It saves the trained model and vectorizer in the `models` folder.

### **`models.py`**

Contains the logic for classifying emails using a machine learning model if present, or falling back to a rule-based approach.

### **`api.py`**

Defines a Flask-based API endpoint (`/classify_email`) that processes an incoming email, applies PII masking, and classifies it into a category using the trained model.

### **`masking/pii_masker.py`**

Contains the code for detecting and masking PII entities using regex patterns for **Aadhar**, **phone number**, **email**, **credit card**, and more. It uses **spaCy** for name entity recognition (NER).

### **`utils.py`**

Contains utility functions for PII masking, including regular expressions to find and mask sensitive information like full names, credit card numbers, and dates of birth.

## How It Works

1. **PII Masking**:  
   The email body is first processed using **PII patterns** to identify sensitive data such as phone numbers, Aadhar numbers, and credit card details. After detection, each entity is masked in the email text, and the masked entities are returned.

2. **Email Classification**:  
   The email body, after masking, is passed through a **machine learning model** that classifies it into categories such as "Purchase", "Support", or "Feedback". If the model is unavailable, a rule-based fallback approach is used for classification.

## Deployment

If you want to deploy this application on a cloud service (e.g., Hugging Face Spaces or Heroku), follow these steps:

1. Create a `requirements.txt` file that includes the required libraries (already provided).
2. Push the code to your preferred cloud service or platform.
3. Ensure the cloud platform has the necessary dependencies installed (e.g., spaCy, scikit-learn).

