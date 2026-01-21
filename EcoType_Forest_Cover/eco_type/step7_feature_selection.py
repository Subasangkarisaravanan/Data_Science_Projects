# =====================================================
# STEP 7: FEATURE SELECTION
# METHOD: RANDOM FOREST FEATURE IMPORTANCE
# VISUAL STUDIO READY
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold

# -----------------------------------------------------
# LOAD FEATURE-ENGINEERED DATASET
# -----------------------------------------------------

DATA_PATH = "data/cover_type_feature_engineered.csv"

df = pd.read_csv(DATA_PATH)

print("Feature-engineered dataset loaded")
print("Dataset shape:", df.shape)
print("-" * 60)

# -----------------------------------------------------
# SEPARATE FEATURES & TARGET
# -----------------------------------------------------

X = df.drop("Cover_Type", axis=1)
y = df["Cover_Type"]

print("Features shape:", X.shape)
print("Target shape:", y.shape)
print("-" * 60)

# -----------------------------------------------------
# HANDLE NaN & INFINITE VALUES (REQUIRED)
# -----------------------------------------------------

X = X.replace([np.inf, -np.inf], np.nan)

imputer = SimpleImputer(strategy="median")

X = pd.DataFrame(
    imputer.fit_transform(X),
    columns=X.columns
)

print("Missing and infinite values handled using median imputation")
print("-" * 60)

# -----------------------------------------------------
# TRAIN RANDOM FOREST (FOR FEATURE IMPORTANCE ONLY)
# -----------------------------------------------------

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

rf.fit(X, y)

print("Random Forest trained for feature importance analysis")
print("-" * 60)

# -----------------------------------------------------
# EXTRACT FEATURE IMPORTANCE
# -----------------------------------------------------

feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Top 15 important features:")
print(feature_importance_df.head(15))
print("-" * 60)

# -----------------------------------------------------
# PLOT FEATURE IMPORTANCE
# -----------------------------------------------------

plt.figure(figsize=(10, 6))
plt.barh(
    feature_importance_df["Feature"][:20],
    feature_importance_df["Importance"][:20]
)
plt.gca().invert_yaxis()
plt.xlabel("Importance")
plt.title("Top 20 Feature Importances (Random Forest)")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# SELECT FEATURES ABOVE IMPORTANCE THRESHOLD
# -----------------------------------------------------

IMPORTANCE_THRESHOLD = 0.005

selected_features = feature_importance_df[
    feature_importance_df["Importance"] >= IMPORTANCE_THRESHOLD
]["Feature"].tolist()

print(f"Features selected (importance >= {IMPORTANCE_THRESHOLD}):")
print("Number of selected features:", len(selected_features))
print("-" * 60)

# -----------------------------------------------------
# OPTIONAL: REMOVE LOW VARIANCE FEATURES
# -----------------------------------------------------

variance_selector = VarianceThreshold(threshold=0.01)
variance_selector.fit(X[selected_features])

low_variance_features = [
    selected_features[i]
    for i in range(len(selected_features))
    if not variance_selector.get_support()[i]
]

print("Low variance features removed:")
print(low_variance_features)
print("-" * 60)

final_features = [
    f for f in selected_features
    if f not in low_variance_features
]

print("Final number of selected features:", len(final_features))
print("-" * 60)

# -----------------------------------------------------
# CREATE FINAL FEATURE-SELECTED DATASET
# -----------------------------------------------------

X_selected = X[final_features]

final_df = X_selected.copy()
final_df["Cover_Type"] = y

print("Final dataset shape after feature selection:")
print(final_df.shape)
print("-" * 60)

# -----------------------------------------------------
# SAVE FEATURE-SELECTED DATASET
# -----------------------------------------------------

OUTPUT_PATH = "data/cover_type_selected_features.csv"

final_df.to_csv(OUTPUT_PATH, index=False)

print(f"Feature-selected dataset saved at: {OUTPUT_PATH}")
print("-" * 60)

print("✅ STEP 7: FEATURE SELECTION COMPLETED SUCCESSFULLY")