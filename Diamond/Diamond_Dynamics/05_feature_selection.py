# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 05_feature_selection.py
# PHASE 4 – FEATURE SELECTION (PROJECT ALIGNED VERSION)
# ==========================================================

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFE
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ----------------------------------------------------------
# Setup folders
# ----------------------------------------------------------
os.makedirs("plots", exist_ok=True)
os.makedirs("data", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 7: FEATURE SELECTION (PROJECT ALIGNED VERSION)")
print("=" * 80)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------
df = pd.read_csv("data/diamonds_step5_feature_engineered.csv")

print("\nDataset Shape:", df.shape)

# ----------------------------------------------------------
# Remove Highly Collinear / Derived Size Features
# ----------------------------------------------------------
features_to_remove = [
    "x", "y", "z",
    "volume",
    "dimension_ratio",
    "carat_category"
]

df = df.drop(columns=features_to_remove, errors="ignore")

print("\nRemoved highly collinear features:")
print(features_to_remove)

# ----------------------------------------------------------
# Separate Target
# ----------------------------------------------------------
y = df["price"]
X = df.drop(columns=["price"])

# ----------------------------------------------------------
# One-Hot Encoding
# ----------------------------------------------------------
X = pd.get_dummies(
    X,
    columns=["cut", "color", "clarity"],
    drop_first=True
)

X = X.astype(float)

print("\nFinal Features Used:")
print(X.columns.tolist())

# ----------------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------------
plt.figure(figsize=(10,8))
sns.heatmap(X.corr(), cmap="coolwarm", center=0)
plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig("plots/feature_selection_correlation_heatmap.png")
plt.show()
plt.close()

# ----------------------------------------------------------
# VIF Calculation
# ----------------------------------------------------------
print("\nCalculating VIF...")

X_vif = sm.add_constant(X)

vif_data = pd.DataFrame()
vif_data["Feature"] = X_vif.columns
vif_data["VIF"] = [
    variance_inflation_factor(X_vif.values, i)
    for i in range(X_vif.shape[1])
]

vif_data = vif_data[vif_data["Feature"] != "const"]
vif_sorted = vif_data.sort_values(by="VIF", ascending=False)

print("\nTop 10 VIF Values:")
print(vif_sorted.head(10))

vif_sorted.to_csv("data/vif_values.csv", index=False)

# ----------------------------------------------------------
# Random Forest Feature Importance
# ----------------------------------------------------------
print("\nTraining Random Forest...")

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X, y)

feature_importances = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nTop 10 Feature Importances:")
print(feature_importances.head(10))

feature_importances.to_csv(
    "data/random_forest_feature_importance.csv",
    index=False
)

plt.figure(figsize=(10,6))
sns.barplot(
    x="Importance",
    y="Feature",
    data=feature_importances.head(15)
)
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig("plots/random_forest_feature_importance.png")
plt.show()
plt.close()

# ----------------------------------------------------------
# Recursive Feature Elimination
# ----------------------------------------------------------
print("\nApplying RFE...")

rfe = RFE(rf, n_features_to_select=10)
rfe.fit(X, y)

selected_features = X.columns[rfe.support_]

print("\nSelected Features by RFE:")
print(selected_features)

pd.DataFrame(
    selected_features,
    columns=["Selected_Features"]
).to_csv(
    "data/rfe_selected_features.csv",
    index=False
)

print("\nSTEP 7 COMPLETED SUCCESSFULLY!")
print("=" * 80)