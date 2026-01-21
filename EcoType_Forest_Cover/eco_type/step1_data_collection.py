# ============================================
# STEP 1: DATA COLLECTION
# ============================================

import pandas as pd

# Load the dataset
df = pd.read_csv("data/cover_type.csv")

print("Dataset loaded successfully!")
print("-" * 50)

# View first few rows
print("First 5 rows of the dataset:")
print(df.head())

print("-" * 50)

# List all columns
print("Column names:")
print(df.columns.tolist())

print("-" * 50)

# Identify target column
print("Target column:")
print("Cover_Type")

print("-" * 50)

# Target class meaning
cover_type_meaning = {
    1: "Spruce/Fir",
    2: "Lodgepole Pine",
    3: "Ponderosa Pine",
    4: "Cottonwood/Willow",
    5: "Aspen",
    6: "Douglas-fir",
    7: "Krummholz"
}

print("Cover Type Classes:")
for key, value in cover_type_meaning.items():
    print(f"{key} -> {value}")