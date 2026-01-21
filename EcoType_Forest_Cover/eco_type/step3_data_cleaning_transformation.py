# ============================================
# STEP 3: DATA CLEANING & TRANSFORMATION (FINAL CORRECTED)
# ============================================

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from scipy.stats import zscore
import matplotlib.pyplot as plt

# --------------------------------------------
# LOAD DATASET
# --------------------------------------------

df = pd.read_csv("data/cover_type.csv")

print("Dataset loaded successfully")
print("-" * 50)

# --------------------------------------------
# TARGET CLASS DISTRIBUTION (VISUAL CHECK)
# --------------------------------------------

print("Class distribution of Cover_Type:")
print(df['Cover_Type'].value_counts().sort_index())
print("-" * 50)

df['Cover_Type'].value_counts().sort_index().plot(kind='bar')
plt.title("Class Distribution of Cover_Type")
plt.xlabel("Cover Type")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.show()

# --------------------------------------------
# SEPARATE FEATURES AND TARGET
# --------------------------------------------

X = df.drop("Cover_Type", axis=1)
y = df["Cover_Type"]

print("Initial feature shape:", X.shape)
print("-" * 50)

# --------------------------------------------
# IDENTIFY COLUMN TYPES (VERY IMPORTANT)
# --------------------------------------------

# Continuous numerical features (safe for outliers & log)
continuous_cols = [
    'Elevation',
    'Aspect',
    'Slope',
    'Horizontal_Distance_To_Hydrology',
    'Horizontal_Distance_To_Roadways',
    'Hillshade_9am',
    'Hillshade_Noon',
    'Hillshade_3pm',
    'Horizontal_Distance_To_Fire_Points'
]

# Categorical features (DO NOT treat as numeric)
categorical_cols = [
    'Wilderness_Area',
    'Soil_Type'
]

print("Continuous columns:", continuous_cols)
print("Categorical columns:", categorical_cols)
print("-" * 50)

# --------------------------------------------
# 1. HANDLE MISSING VALUES (IMPUTATION)
# --------------------------------------------

imputer = SimpleImputer(strategy="median")

X_imputed = pd.DataFrame(
    imputer.fit_transform(X),
    columns=X.columns
)

print("Missing values handled using MEDIAN imputation")
print("-" * 50)

# --------------------------------------------
# 2. OUTLIER DETECTION (Z-SCORE) – CONTINUOUS ONLY
# --------------------------------------------

z_scores = X_imputed[continuous_cols].apply(zscore)
outlier_counts = (z_scores.abs() > 3).sum()

print("Potential outliers detected using Z-score (continuous columns only):")
print(outlier_counts[outlier_counts > 0])
print("-" * 50)

# --------------------------------------------
# 3. OUTLIER HANDLING (IQR METHOD) – CONTINUOUS ONLY
# --------------------------------------------

def remove_outliers_iqr(df, columns):
    df_clean = df.copy()
    for col in columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_clean = df_clean[
            (df_clean[col] >= lower) & (df_clean[col] <= upper)
        ]
    return df_clean

X_no_outliers = remove_outliers_iqr(X_imputed, continuous_cols)
y = y.loc[X_no_outliers.index]

print("Outliers handled using IQR method")
print("New feature shape:", X_no_outliers.shape)
print("-" * 50)

# --------------------------------------------
# 4. FIX SKEWNESS (LOG TRANSFORMATION)
# --------------------------------------------
# Apply ONLY to continuous columns with non-negative values

X_transformed = X_no_outliers.copy()

for col in continuous_cols:
    if (X_transformed[col] >= 0).all():
        X_transformed[col] = np.log1p(X_transformed[col])

print("Skewness reduced using log1p transformation (safe columns only)")
print("-" * 50)

# --------------------------------------------
# FINAL CHECK
# --------------------------------------------

print("Final cleaned feature shape:", X_transformed.shape)
print("Target shape:", y.shape)
print("-" * 50)

print("✅ Data Cleaning & Transformation COMPLETED SUCCESSFULLY")

# --------------------------------------------
# SAVE CLEANED DATASET FOR NEXT STEPS
# --------------------------------------------

cleaned_df = X_transformed.copy()
cleaned_df['Cover_Type'] = y

cleaned_df.to_csv("data/cover_type_cleaned.csv", index=False)

print("✅ Cleaned dataset saved as data/cover_type_cleaned.csv")
