# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 07_regression_models.py
# STEP 9 – REGRESSION MODEL TRAINING (FINAL PROFESSIONAL)
# ==========================================================

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ----------------------------------------------------------
# Setup folders
# ----------------------------------------------------------
os.makedirs("plots", exist_ok=True)
os.makedirs("models", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 9: REGRESSION MODEL TRAINING (FINAL PROFESSIONAL)")
print("=" * 80)

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

# Scaled (for linear-based models)
X_train_scaled = pd.read_csv("data/X_train_scaled.csv")
X_test_scaled = pd.read_csv("data/X_test_scaled.csv")

# Unscaled (for tree models)
df = pd.read_csv("data/diamonds_step5_feature_engineered.csv")

# Apply same preprocessing as Step 8
columns_to_remove = ["x", "y", "z", "volume", "dimension_ratio", "carat_category"]
df = df.drop(columns=columns_to_remove, errors="ignore")

df_encoded = pd.get_dummies(
    df,
    columns=["cut", "color", "clarity"],
    drop_first=True
)

selected_features = pd.read_csv(
    "data/rfe_selected_features.csv"
)["Selected_Features"].tolist()

X = df_encoded[selected_features]
y = df_encoded["price"]

from sklearn.model_selection import train_test_split
X_train_unscaled, X_test_unscaled, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

y_train = y_train.values.ravel()
y_test = y_test.values.ravel()

# ----------------------------------------------------------
# Models
# ----------------------------------------------------------

models = {
    "Linear_Regression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.001),
    "KNN": KNeighborsRegressor(),
    "Decision_Tree": DecisionTreeRegressor(random_state=42),
    "Random_Forest": RandomForestRegressor(n_estimators=200, random_state=42),
    "XGBoost": XGBRegressor(random_state=42, verbosity=0)
}

results = []
best_r2 = -np.inf
best_model = None
best_model_name = None

# ----------------------------------------------------------
# Training Loop
# ----------------------------------------------------------

for name, model in models.items():

    print(f"\nTraining {name}...")

    # Use scaled data for linear-type models
    if name in ["Linear_Regression", "Ridge", "Lasso", "KNN"]:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        n = X_test_scaled.shape[0]
        p = X_test_scaled.shape[1]
    else:
        model.fit(X_train_unscaled, y_train)
        y_pred = model.predict(X_test_unscaled)
        n = X_test_unscaled.shape[0]
        p = X_test_unscaled.shape[1]

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    results.append([name, mae, mse, rmse, r2, adjusted_r2])

    # Save trained model
    joblib.dump(model, f"models/{name}.pkl")

    print(f"{name} Performance:")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2: {r2:.4f}")
    print(f"Adjusted R2: {adjusted_r2:.4f}")

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name

# ----------------------------------------------------------
# Save Best Model
# ----------------------------------------------------------

print(f"\nBest Model: {best_model_name} (R2 = {best_r2:.4f})")
joblib.dump(best_model, "models/best_regression_model.pkl")

# ----------------------------------------------------------
# Results Table
# ----------------------------------------------------------

results_df = pd.DataFrame(
    results,
    columns=["Model", "MAE", "MSE", "RMSE", "R2", "Adjusted_R2"]
)

print("\nModel Comparison:")
print(results_df.sort_values(by="R2", ascending=False))

results_df.to_csv("data/regression_model_results.csv", index=False)

# ----------------------------------------------------------
# Comparison Plot
# ----------------------------------------------------------

plt.figure(figsize=(10, 6))
sns.barplot(x="Model", y="R2", data=results_df)
plt.xticks(rotation=45)
plt.title("Regression Model Comparison (R2)")
plt.tight_layout()
plt.savefig("plots/regression_model_comparison.png")
plt.show()

print("\nSTEP 9 COMPLETED SUCCESSFULLY!")
print("=" * 80)