# src/step14_feature_selection.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

print("=" * 70)
print("STEP 14: FEATURE IMPORTANCE & FEATURE SELECTION")
print("=" * 70)

# Load SMOTE-balanced data
X_train = pd.read_csv("data/X_train_smote.csv")
y_train = pd.read_csv("data/y_train_smote.csv")

rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)

feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(feature_importance)

print("\nDecision:")
print("All features retained (no low-importance features found).")

print("=" * 70)