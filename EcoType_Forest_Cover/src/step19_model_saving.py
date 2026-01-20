# src/step21_model_saving.py

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier

print("=" * 70)
print("STEP 21: FINAL MODEL TRAINING & SAVING")
print("=" * 70)

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Load data
X_train = pd.read_csv("data/X_train_smote.csv")
y_train = pd.read_csv("data/y_train_smote.csv").values.ravel()

print("Training data loaded:")
print("X_train shape:", X_train.shape)

# Best parameters (taken from Step 18 output)
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

print("Training final Random Forest model...")
model.fit(X_train, y_train)

# Save model
model_path = "models/best_model.pkl"
joblib.dump(model, model_path)

print(f"\n✅ Model saved successfully at: {model_path}")
print("=" * 70)