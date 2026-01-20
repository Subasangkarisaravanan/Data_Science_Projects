# src/step08_skewness_handling.py
import pandas as pd
import numpy as np

df = pd.read_csv("data/forest_outlier_handled.csv")

skew_cols = [
    "Horizontal_Distance_To_Hydrology",
    "Horizontal_Distance_To_Roadways",
    "Horizontal_Distance_To_Fire_Points"
]

for col in skew_cols:
    df[col] = np.log1p(df[col])

df.to_csv("data/forest_skewness_handled.csv", index=False)
print("Skewness fixed")