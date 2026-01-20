# src/step13_smote_handling.py

import pandas as pd
from imblearn.over_sampling import SMOTE

print("=" * 70)
print("STEP 13: CLASS IMBALANCE HANDLING USING SMOTE")
print("=" * 70)

X_train = pd.read_csv("data/X_train.csv")
y_train = pd.read_csv("data/y_train.csv")

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Save SMOTE outputs
X_train_res.to_csv("data/X_train_smote.csv", index=False)
y_train_res.to_csv("data/y_train_smote.csv", index=False)

print("SMOTE applied successfully")
print("Balanced training data shape:", X_train_res.shape)

print("=" * 70)