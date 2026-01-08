import pandas as pd

print("\n====== STEP 1: LOAD DATA ======\n")

obesity_df = pd.read_csv("df_obesity_clean.csv")
malnutrition_df = pd.read_csv("df_malnutrition_clean.csv")

print("Obesity Shape:", obesity_df.shape)
print("Malnutrition Shape:", malnutrition_df.shape)


print("\n====== STEP 2: CHECK MISSING VALUES ======\n")

print("\nObesity Missing Values:\n", obesity_df.isna().sum())
print("\nMalnutrition Missing Values:\n", malnutrition_df.isna().sum())


print("\n====== STEP 3: REGION MISSING SUMMARY ======\n")

def show_region_missing(df, label):
    total = len(df)
    missing = df['Region'].isna().sum()
    print(f"\n📌 {label}")
    print(f"Total Rows      = {total}")
    print(f"Missing Regions = {missing} ({missing/total*100:.2f}%)")

show_region_missing(obesity_df, "Obesity Dataset")
show_region_missing(malnutrition_df, "Malnutrition Dataset")


print("\n====== STEP 4: BASIC NUMERIC SUMMARY ======\n")

print("\n📊 Obesity Mean_Estimate Summary")
print(obesity_df['Mean_Estimate'].describe())

print("\n📊 Malnutrition Mean_Estimate Summary")
print(malnutrition_df['Mean_Estimate'].describe())


print("\n====== ANALYSIS COMPLETE (NO DATA MODIFIED) ======\n")