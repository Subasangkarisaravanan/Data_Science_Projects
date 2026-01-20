# src/step07_outlier_handling.py

import pandas as pd
import numpy as np

print("=" * 70)
print("STEP 07: OUTLIER DETECTION & HANDLING (IQR METHOD)")
print("=" * 70)

# Load dataset
df = pd.read_csv("data/forest_cover.csv")

# Select only numeric columns (Cover_Type is object, so excluded automatically)
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

print("\nNumeric columns considered for outlier handling:")
print(list(numeric_cols))

# IQR-based capping
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df[col] = np.clip(df[col], lower_bound, upper_bound)

# Save cleaned data
df.to_csv("data/forest_outlier_handled.csv", index=False)

print("\nOutliers handled using IQR method.")
print("Cleaned file saved as: data/forest_outlier_handled.csv")

print("\n" + "=" * 70)
print("OUTLIER HANDLING COMPLETED SUCCESSFULLY")
print("=" * 70)