import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import joblib

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Load your dataset (must have 'email' and 'category' columns)
df = pd.read_csv("data/emails.csv")
df.dropna(subset=["email", "type"], inplace=True)

X = df["email"]
y = df["type"]

# Build pipeline: TF-IDF + RandomForest
pipeline = make_pipeline(
    TfidfVectorizer(stop_words="english"),
    RandomForestClassifier(n_estimators=100, random_state=42),
)

# Train/test split for evaluation (optional)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
pipeline.fit(X_train, y_train)

# Save pipeline as single model
joblib.dump(pipeline, "models/email_classifier.pkl")
print("Model saved to models/email_classifier.pkl")


# Save the trained model
joblib.dump(pipeline, "models/email_classifier.pkl", compress=3)

print("Model saved to 'models/email_classifier.pkl'")
