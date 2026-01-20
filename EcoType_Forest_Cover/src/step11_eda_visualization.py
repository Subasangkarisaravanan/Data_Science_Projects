# src/step11_eda_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 70)
print("STEP 11: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 70)

# Load processed data (after encoding & feature engineering)
df = pd.read_csv("data/final_processed_data.csv")

# ---------------------------------
# 1️⃣ TARGET VARIABLE DISTRIBUTION
# ---------------------------------
plt.figure(figsize=(8, 5))
sns.countplot(x="Cover_Type", data=df)
plt.title("Target Variable Distribution (Cover_Type)")
plt.xlabel("Cover Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ---------------------------------
# 2️⃣ HISTOGRAMS – NUMERICAL FEATURES
# ---------------------------------
numerical_features = df.drop("Cover_Type", axis=1).columns

df[numerical_features].hist(
    figsize=(16, 12),
    bins=30,
    edgecolor="black"
)
plt.suptitle("Histograms of Numerical Features", fontsize=16)
plt.tight_layout()
plt.show()

# ---------------------------------
# 3️⃣ BOXPLOTS – OUTLIER VISUALIZATION
# ---------------------------------
plt.figure(figsize=(16, 6))
sns.boxplot(data=df[numerical_features])
plt.title("Boxplot of Numerical Features (After Outlier Handling)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ---------------------------------
# 4️⃣ CORRELATION HEATMAP
# ---------------------------------
plt.figure(figsize=(12, 8))
corr_matrix = df[numerical_features].corr()

sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    linewidths=0.5
)
plt.title("Correlation Heatmap of Numerical Features")
plt.tight_layout()
plt.show()

# ---------------------------------
# 5️⃣ BIVARIATE ANALYSIS (Feature vs Target)
# ---------------------------------
plt.figure(figsize=(8, 5))
sns.boxplot(x="Cover_Type", y="Elevation", data=df)
plt.title("Elevation vs Cover Type")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.boxplot(x="Cover_Type", y="Slope", data=df)
plt.title("Slope vs Cover Type")
plt.tight_layout()
plt.show()

print("\nEDA VISUALIZATION COMPLETED SUCCESSFULLY")
print("=" * 70)