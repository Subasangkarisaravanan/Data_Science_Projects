import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("\n====== STEP 1: LOAD CLEANED DATA ======\n")

obesity_df = pd.read_csv("df_obesity_clean.csv")
malnutrition_df = pd.read_csv("df_malnutrition_clean.csv")


print("\n====== STEP 2: MISSING REGION CHECK ======\n")

print("Before Fix — Obesity Missing Regions:", obesity_df['Region'].isna().sum())
print("Before Fix — Malnutrition Missing Regions:", malnutrition_df['Region'].isna().sum())


print("\n====== STEP 3: APPLY REGION FIX ======\n")

obesity_df['Region'].fillna('Unknown', inplace=True)
malnutrition_df['Region'].fillna('Unknown', inplace=True)

print("After Fix — Obesity Missing Regions:", obesity_df['Region'].isna().sum())
print("After Fix — Malnutrition Missing Regions:", malnutrition_df['Region'].isna().sum())


print("\n====== STEP 4: DISTRIBUTION PLOTS ======\n")

plt.figure()
sns.histplot(obesity_df['Mean_Estimate'], kde=True)
plt.title("Obesity Mean Estimate Distribution")
plt.show()

plt.figure()
sns.histplot(malnutrition_df['Mean_Estimate'], kde=True)
plt.title("Malnutrition Mean Estimate Distribution")
plt.show()


print("\n====== STEP 5: GENDER BOXPLOTS ======\n")

plt.figure()
sns.boxplot(x='Gender', y='Mean_Estimate', data=obesity_df)
plt.title("Obesity by Gender")
plt.show()

plt.figure()
sns.boxplot(x='Gender', y='Mean_Estimate', data=malnutrition_df)
plt.title("Malnutrition by Gender")
plt.show()


print("\n====== STEP 6: GLOBAL TREND OVER YEARS ======\n")

ob_trend = obesity_df.groupby('Year')['Mean_Estimate'].mean()
mal_trend = malnutrition_df.groupby('Year')['Mean_Estimate'].mean()

plt.figure()
ob_trend.plot()
plt.title("Global Obesity Trend Over Years")
plt.ylabel("Avg Mean Estimate")
plt.show()

plt.figure()
mal_trend.plot()
plt.title("Global Malnutrition Trend Over Years")
plt.ylabel("Avg Mean Estimate")
plt.show()


print("\n====== STEP 7: SAVE FINAL CLEAN FILES ======\n")

obesity_df.to_csv("df_obesity_clean_verified.csv", index=False)
malnutrition_df.to_csv("df_malnutrition_clean_verified.csv", index=False)

print("🎉 Final validated datasets saved successfully")