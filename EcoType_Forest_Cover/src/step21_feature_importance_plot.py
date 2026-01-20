# src/step20_feature_importance_plot.py

import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

print("=" * 70)
print("STEP 20: FEATURE IMPORTANCE VISUALIZATION")
print("=" * 70)

# Resolve paths safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")

# Load model
model = joblib.load(MODEL_PATH)

# Load training data to get feature names
X_train = pd.read_csv("data/X_train_smote.csv")

# Extract feature importance
importances = model.feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": importances
}).sort_values(by="Importance", ascending=True)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df["Feature"], feature_importance_df["Importance"])
plt.title("Feature Importance - Random Forest")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

print("\nFeature importance plot displayed successfully.")
print("=" * 70)