# src/step03_data_understanding.py
import pandas as pd

df = pd.read_csv("data/forest_cover.csv")
print(df.info())
print(df.describe())