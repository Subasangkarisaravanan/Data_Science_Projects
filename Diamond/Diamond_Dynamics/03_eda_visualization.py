# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 03_eda_visualization.py
# STEP 5: EXPLORATORY DATA ANALYSIS (FINAL SHOW + SAVE VERSION)
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pandas.plotting import scatter_matrix

# ----------------------------------------------------------
# Global Settings
# ----------------------------------------------------------
sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)

print("\n" + "=" * 80)
print("STEP 5: EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# ----------------------------------------------------------
# Create plots directory
# ----------------------------------------------------------
os.makedirs("plots", exist_ok=True)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------
df = pd.read_csv("data/diamonds_step4_transformed.csv")
print("\nDataset Shape:", df.shape)

# ----------------------------------------------------------
# Define Columns
# ----------------------------------------------------------
numeric_cols = ["carat", "depth", "table", "price", "x", "y", "z"]
categorical_cols = ["cut", "color", "clarity"]

# Logical ordering for categorical variables
cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
color_order = sorted(df["color"].unique())
clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

order_dict = {
    "cut": cut_order,
    "color": color_order,
    "clarity": clarity_order
}

# ==========================================================
# 1️⃣ Distribution Plots
# ==========================================================

print("\nGenerating Distribution Plots...")

for col in numeric_cols:
    plt.figure(figsize=(7, 4))
    sns.histplot(df[col], kde=True, bins=40)
    plt.title(f"Distribution of {col}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"plots/distribution_{col}.png")
    plt.show()
    plt.close()

# ==========================================================
# 2️⃣ Standalone Price Boxplot (Optional Enhancement)
# ==========================================================

print("Generating Standalone Price Boxplot...")

plt.figure(figsize=(6, 4))
sns.boxplot(y=df["price"])
plt.title("Boxplot of Log Transformed Price", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/boxplot_price_only.png")
plt.show()
plt.close()

# ==========================================================
# 3️⃣ Count Plots
# ==========================================================

print("Generating Count Plots...")

for col in categorical_cols:
    plt.figure(figsize=(7, 4))
    sns.countplot(
        x=col,
        data=df,
        order=order_dict[col]
    )
    plt.title(f"Count Plot of {col}", fontsize=13, fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"plots/countplot_{col}.png")
    plt.show()
    plt.close()

# ==========================================================
# 4️⃣ Boxplots (Price vs Categories)
# ==========================================================

print("Generating Boxplots for Price vs Categories...")

for col in categorical_cols:
    plt.figure(figsize=(8, 5))
    sns.boxplot(
        x=col,
        y="price",
        data=df,
        order=order_dict[col]
    )
    plt.title(f"Log Price vs {col}", fontsize=13, fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"plots/boxplot_price_vs_{col}.png")
    plt.show()
    plt.close()

# ==========================================================
# 5️⃣ Correlation Heatmap
# ==========================================================

print("Generating Correlation Heatmap...")

plt.figure(figsize=(10, 8))
corr_matrix = df[numeric_cols].corr()

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    center=0
)

plt.title("Correlation Heatmap", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/correlation_heatmap.png")
plt.show()
plt.close()

# ==========================================================
# 6️⃣ Carat vs Price Regression Plot
# ==========================================================

print("Generating Carat vs Price Regression Plot...")

plt.figure(figsize=(7, 5))
sns.regplot(
    x="carat",
    y="price",
    data=df,
    scatter_kws={"alpha": 0.4},
    line_kws={"color": "red"}
)

plt.title("Carat vs Log Price Relationship", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/carat_vs_price.png")
plt.show()
plt.close()

# ==========================================================
# 7️⃣ Pairplot
# ==========================================================

print("Generating Pairplot...")

pairplot = sns.pairplot(
    df[["carat", "x", "y", "z", "price", "cut"]],
    hue="cut",
    corner=True
)

pairplot.fig.suptitle("Pairplot Colored by Cut", y=1.02)
pairplot.savefig("plots/pairplot.png")
plt.show()
plt.close()

# ==========================================================
# 8️⃣ Scatter Plot Matrix
# ==========================================================

print("Generating Scatter Plot Matrix...")

scatter_matrix(
    df[["carat", "x", "y", "z", "price"]],
    alpha=0.3,
    figsize=(10, 8),
    diagonal="kde"
)

plt.suptitle("Scatter Plot Matrix", fontsize=15)
plt.tight_layout()
plt.savefig("plots/scatter_plot_matrix.png")
plt.show()
plt.close()

# ==========================================================
# COMPLETION
# ==========================================================

print("\nAll plots saved successfully inside 'plots' folder.")
print("STEP 5 COMPLETED SUCCESSFULLY!")
print("=" * 80)