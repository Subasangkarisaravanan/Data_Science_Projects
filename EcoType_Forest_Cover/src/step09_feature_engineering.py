# src/step09_feature_engineering.py
import pandas as pd

df = pd.read_csv("data/forest_skewness_handled.csv")

df["Hydrology_Ratio"] = df["Horizontal_Distance_To_Hydrology"] / (abs(df["Vertical_Distance_To_Hydrology"]) + 1)
df["Hillshade_Diff"] = df["Hillshade_Noon"] - df["Hillshade_9am"]

df.to_csv("data/forest_engineered.csv", index=False)
print("Derived features added")