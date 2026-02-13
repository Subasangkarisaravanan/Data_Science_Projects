# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 06_model_preparation.py
# STEP 8 – FINAL MODEL PREPARATION (ALIGNED VERSION)
# ==========================================================

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ----------------------------------------------------------
# Setup folders
# ----------------------------------------------------------
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 8: FINAL MODEL PREPARATION (ALIGNED WITH FEATURE SELECTION)")
print("=" * 80)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------
df = pd.read_csv("data/diamonds_step5_feature_engineered.csv")

# ----------------------------------------------------------
# Remove Same Columns as Feature Selection
# ----------------------------------------------------------
columns_to_remove = [
    "x", "y", "z",
    "volume",
    "dimension_ratio",
    "carat_category"
]

df = df.drop(columns=columns_to_remove, errors="ignore")

# ----------------------------------------------------------
# One-Hot Encoding (Same as Step 7)
# ----------------------------------------------------------
df_encoded = pd.get_dummies(
    df,
    columns=["cut", "color", "clarity"],
    drop_first=True
)

df_encoded = df_encoded.astype(float)

# ----------------------------------------------------------
# Load RFE Selected Features
# ----------------------------------------------------------
selected_features = pd.read_csv(
    "data/rfe_selected_features.csv"
)["Selected_Features"].tolist()

print("\nUsing RFE Selected Features:")
print(selected_features)

# ----------------------------------------------------------
# Prepare X and y
# ----------------------------------------------------------
X = df_encoded[selected_features]
y = df_encoded["price"]

# ----------------------------------------------------------
# Train-Test Split
# ----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTrain Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

# ----------------------------------------------------------
# Scaling (For Linear Models)
# ----------------------------------------------------------
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------------------------------------------------
# Save Prepared Data
# ----------------------------------------------------------
pd.DataFrame(X_train_scaled, columns=X_train.columns)\
    .to_csv("data/X_train_scaled.csv", index=False)

pd.DataFrame(X_test_scaled, columns=X_test.columns)\
    .to_csv("data/X_test_scaled.csv", index=False)

y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

# Save scaler
joblib.dump(scaler, "models/regression_scaler.pkl")

# Save feature order (critical for deployment)
joblib.dump(X_train.columns.tolist(), "models/feature_columns.pkl")

print("\nScaler saved.")
print("Feature columns saved.")
print("\nSTEP 8 COMPLETED SUCCESSFULLY!")
print("=" * 80)