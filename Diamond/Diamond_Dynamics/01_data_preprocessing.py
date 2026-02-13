# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 01_data_preprocessing.py
# PHASE 1: DATA CLEANING & PREPROCESSING (FINAL CORRECTED)
# ==========================================================

import pandas as pd
import os

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

print("\n" + "=" * 80)
print("💎 DIAMOND DYNAMICS - DATA PREPROCESSING STARTED")
print("=" * 80)

# ==========================================================
# STEP 1: LOAD DATA
# ==========================================================

print("\nSTEP 1: DATA LOADING & INSPECTION")
print("-" * 80)

try:
    df = pd.read_csv("data/diamonds.csv")
    print("Dataset loaded successfully.")
except Exception as e:
    print("Error loading dataset:", e)
    raise

print("\nInitial Shape:", df.shape)

# -----------------------------
# Missing Values
# -----------------------------
print("\nMissing Values:")
print(df.isnull().sum())

# -----------------------------
# Duplicate Rows
# -----------------------------
duplicate_count = df.duplicated().sum()
print("\nDuplicate Rows:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates().reset_index(drop=True)
    print("Duplicates removed.")
    print("New Shape:", df.shape)

# -----------------------------
# Data Types
# -----------------------------
print("\nColumn Data Types:")
print(df.dtypes)

# ==========================================================
# STEP 2: INVALID DIMENSIONS (x, y, z = 0)
# ==========================================================

print("\nSTEP 2: INVALID DIMENSION HANDLING")
print("-" * 80)

invalid_mask = (df["x"] == 0) | (df["y"] == 0) | (df["z"] == 0)
invalid_count = invalid_mask.sum()

print("Invalid rows found:", invalid_count)
print(f"Percentage affected: {(invalid_count / len(df)) * 100:.4f}%")

# Remove invalid rows (very small percentage)
df = df.loc[~invalid_mask].reset_index(drop=True)

print("Shape after removing invalid dimensions:", df.shape)
print("Minimum x, y, z values after cleaning:")
print(df[["x", "y", "z"]].min())

# Save intermediate cleaned dataset
os.makedirs("data", exist_ok=True)
df.to_csv("data/diamonds_step2_cleaned.csv", index=False)

# ==========================================================
# STEP 3: OUTLIER DETECTION USING IQR (SAFE VERSION)
# ==========================================================

print("\nSTEP 3: OUTLIER DETECTION (IQR METHOD)")
print("-" * 80)

numerical_cols = ["carat", "depth", "table", "price", "x", "y", "z"]

bounds = {}

for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    bounds[col] = (lower, upper)

    outliers = ((df[col] < lower) | (df[col] > upper)).sum()

    print(f"\nColumn: {col}")
    print(f"Lower Bound: {lower:.2f}")
    print(f"Upper Bound: {upper:.2f}")
    print(f"Outliers Detected: {outliers}")

# -----------------------------
# Remove Outliers (Combined Mask)
# -----------------------------
outlier_mask = pd.Series(True, index=df.index)

for col in numerical_cols:
    lower, upper = bounds[col]
    outlier_mask &= df[col].between(lower, upper)

df_clean = df.loc[outlier_mask].reset_index(drop=True)

print("\nShape after removing outliers:", df_clean.shape)

# Save final cleaned dataset
df_clean.to_csv("data/diamonds_step3_no_outliers.csv", index=False)

print("\nSTEP 3 COMPLETED SUCCESSFULLY!")
print("\n" + "=" * 80)
print("💎 DATA PREPROCESSING COMPLETED SUCCESSFULLY")
print("=" * 80)