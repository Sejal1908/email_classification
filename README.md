# email_Classification_support_Sejal
A Python-based Flask API that detects and masks Personally Identifiable Information (PII) in email content and classifies the email into relevant categories using a machine learning model. This project is deployed via Hugging Face Spaces.

🚀 Demo
Paste your email content into the API via a POST request, and get back a masked version with all sensitive entities hidden, alongside the predicted email category.

----------------------------------------------------------------------------------------

🔍 Features
✅ Regex and NER-based PII Masking (name, email, phone number, DOB, etc.)

🤖 ML-based Email Classification (e.g., General, Finance, Promotions)

📡 REST API built using Flask

🧪 Ready-to-test JSON response format

☁️ Hosted on Hugging Face Spaces with GitHub integration

--------------------------------------------------------------------------------------------
📂 Project Structure

.
├── app.py                  # Main Flask app entrypoint
├── api.py                  # API routes and logic
└── data/
   └── emails.csv         # the Data set 
├── models.py               # Classification logic and ML model
├── utils.py                # PII masking functions
├── train_model.py          # Script to train and save ML model
├── requirements.txt        # Required Python dependencies
├── README.md               # You're here!
├── space.yaml              # Hugging Face deployment file
├── test_input.json         # Sample input for testing
└── model/
    └── email_classifier.pkl      # Pretrained ML model

-----------------------------------------------------------------------------------------

🧠 Technologies Used
Python 3.10

Flask

Scikit-learn

Regex + SpaCy (for PII detection)


Docker + Hugging Face Spaces

GitHub (CI/CD)

 ------------------------------------------------------------------------------------------

 🔧 Installation (Run Locally)

 # Clone the repository
git clone https://github.com/Sejal1908/email-classification-api.git
cd email-classification-api

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

-------------------------------------------------------------------------------

🧪 API Usage

I have used postman for this project

▶️ Endpoint
POST /classify_email

▶️ Request Headers
pgsql
Copy code
Content-Type: application/json

▶️ Request Body
json
Copy code
{
  "email": "Contact Alice Wonderland at alice@wonder.land or +91 98765 43210. DOB: 01/01/1980."
}

✅ Successful Response Format
json
Copy code
{
  "input_email_body": "Contact Alice Wonderland at alice@wonder.land or +91 98765 43210. DOB: 01/01/1980.",
  "list_of_masked_entities": [
    {
      "position": [0, 24],
      "classification": "full_name",
      "entity": "Contact Alice Wonderland"
    },
    {
      "position": [28, 45],
      "classification": "email",
      "entity": "alice@wonder.land"
    },
    {
      "position": [49, 64],
      "classification": "phone_number",
      "entity": "+91 98765 43210"
    },
    {
      "position": [71, 81],
      "classification": "dob",
      "entity": "01/01/1980"
    }
  ],
  "masked_email": "[full_name] at [email] or [phone_number]. DOB: [dob].",
  "category_of_the_email": "General"
}

-------------------------------------------------------------------------------------

⚙️ Hugging Face Deployment

Go to https://huggingface.co/spaces and click "Create Space"

Choose SDK as Docker

Select "Link to GitHub Repository"

Ensure you include a space.yaml or README.md for Hugging Face to build correctly

Push your code to GitHub — it auto-deploys!

Example space.yaml

# This file tells Hugging Face Spaces how to run your app
sdk: docker
python_version: "3.10"
---------------------------------------------------------------------------------------
🧠 Training the Classifier

You can train and save your ML model using the provided train_model.py script.

bash
Copy code
python train_model.py
This will generate a classifier.pkl saved in the /model folder which your app will load at runtime.

-----------------------------------------------------------------------------------------------------

DockerFile

# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]

--------------------------------------------------------------------------------------------

Docker Setup

1. Build the Docker image:
docker build -t email-classification-api .

2. Run the Docker container:
docker run -p 7860:7860 email-classification-api

3. Access the application on http://localhost:7860.
--------------------------------------------------------------------------------------------
📜 License

This project is licensed under the MIT License 
--------------------------------------------------------------------------------------------

👩‍💻 Author
Sejal Vhankade
🔗 [Github](https://github.com/Sejal1908)
🔗 [LinkedIn](https://www.linkedin.com/in/sejalvhankade/)
✉️ sejal.vhankade@gmail.com


