# ============================================
# STEP 2: DATA UNDERSTANDING
# ============================================

import pandas as pd

# Load dataset
df = pd.read_csv("data/cover_type.csv")

print("Dataset Shape (rows, columns):")
print(df.shape)
print("-" * 50)

# Dataset structure
print("Dataset Information:")
df.info()
print("-" * 50)

# Statistical summary
print("Statistical Summary:")
print(df.describe())
print("-" * 50)

# Check missing values
print("Missing values per column:")
print(df.isnull().sum())
print("-" * 50)

# Check duplicate rows
duplicate_count = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")
print("-" * 50)

# Class distribution
print("Class Distribution (Cover_Type):")
class_counts = df['Cover_Type'].value_counts().sort_index()
print(class_counts)
print("-" * 50)

# Percentage distribution
print("Class Distribution Percentage:")
class_percentage = df['Cover_Type'].value_counts(normalize=True).sort_index() * 100
print(class_percentage)