# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 04_feature_engineering.py
# PHASE 3 – FEATURE ENGINEERING (FINAL SAFE VERSION)
# ==========================================================

import pandas as pd
import numpy as np
import os

print("\n" + "=" * 80)
print("STEP 6: FEATURE ENGINEERING (FINAL SAFE VERSION)")
print("=" * 80)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------
df = pd.read_csv("data/diamonds_step4_transformed.csv")

print("\nDataset Shape Before Feature Engineering:")
print(df.shape)

# ==========================================================
# 1️⃣ Volume Feature
# ==========================================================

df["volume"] = df["x"] * df["y"] * df["z"]
print("Volume feature created.")

# ==========================================================
# 2️⃣ Dimension Ratio Feature
# ==========================================================

df["dimension_ratio"] = (df["x"] + df["y"]) / (2 * df["z"])
print("Dimension ratio feature created.")

# ==========================================================
# 3️⃣ Carat Category Feature
# ==========================================================

def carat_category(carat):
    if carat < 0.5:
        return "Light"
    elif carat <= 1.5:
        return "Medium"
    else:
        return "Heavy"

df["carat_category"] = df["carat"].apply(carat_category)
print("Carat category feature created.")

# ==========================================================
# Verify Added Columns
# ==========================================================

print("\nNew Columns Added:")
print(df[["volume", "dimension_ratio", "carat_category"]].head())

print("\nDataset Shape After Feature Engineering:")
print(df.shape)

# ----------------------------------------------------------
# Save Dataset
# ----------------------------------------------------------
os.makedirs("data", exist_ok=True)
df.to_csv("data/diamonds_step5_feature_engineered.csv", index=False)

print("\nSTEP 6 COMPLETED SUCCESSFULLY!")
print("=" * 80)