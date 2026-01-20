# src/step19_model_evaluation.py

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

print("=" * 70)
print("STEP 19: MODEL EVALUATION")
print("=" * 70)

# Safe path handling
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")

# Load test data
X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv").values.ravel()

# Load model
model = joblib.load(MODEL_PATH)

# Predict
preds = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))

print("\nClassification Report:")
print(classification_report(y_test, preds))

print("=" * 70)