# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 02_skewness_and_transformation.py
# PHASE 1 – STEP 4: SKEWNESS CHECK & LOG TRANSFORMATION (FINAL CORRECTED)
# ==========================================================

import pandas as pd
import numpy as np
import os

pd.set_option("display.max_columns", None)

print("\n" + "=" * 80)
print("STEP 4: SKEWNESS CHECK & LOG TRANSFORMATION")
print("=" * 80)

# ==========================================================
# LOAD CLEANED DATA
# ==========================================================

df = pd.read_csv("data/diamonds_step3_no_outliers.csv")

print("\nDataset Shape:", df.shape)

# ==========================================================
# CHECK SKEWNESS
# ==========================================================

numerical_cols = ["carat", "depth", "table", "price", "x", "y", "z"]

print("\nSkewness Before Transformation:")
skewness_values = df[numerical_cols].skew()
print(skewness_values)

# ==========================================================
# IDENTIFY HIGHLY SKEWED FEATURES
# ==========================================================

skew_threshold = 1  # Industry standard threshold

skewed_columns = skewness_values[
    abs(skewness_values) > skew_threshold
    ].index.tolist()

print("\nColumns with |skewness| > 1:")
print(skewed_columns)

# ==========================================================
# APPLY LOG1P TRANSFORMATION (SAFE)
# ==========================================================

for col in skewed_columns:
    if (df[col] <= -1).any():
        raise ValueError(f"Cannot apply log1p to column {col} due to invalid values.")

    df[col] = np.log1p(df[col])
    print(f"Applied log1p transformation to: {col}")

# ==========================================================
# VERIFY SKEWNESS AFTER TRANSFORMATION
# ==========================================================

print("\nSkewness After Transformation:")
print(df[numerical_cols].skew())

# ==========================================================
# SAVE TRANSFORMED DATA
# ==========================================================

os.makedirs("data", exist_ok=True)
df.to_csv("data/diamonds_step4_transformed.csv", index=False)

print("\nSTEP 4 COMPLETED SUCCESSFULLY!")
print("=" * 80)