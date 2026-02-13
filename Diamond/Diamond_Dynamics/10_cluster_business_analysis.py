# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 10_cluster_business_analysis.py
# STEP 12 – BUSINESS INTERPRETATION OF MARKET SEGMENTS
# ==========================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------
# Setup
# ----------------------------------------------------------
os.makedirs("plots", exist_ok=True)
os.makedirs("data", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 12: BUSINESS ANALYSIS OF MARKET SEGMENTS")
print("=" * 80)

# ----------------------------------------------------------
# Load Segmented Dataset
# ----------------------------------------------------------
df = pd.read_csv("data/diamonds_segmented.csv")

# ----------------------------------------------------------
# Convert Log Price Back to USD
# ----------------------------------------------------------
df["price_usd"] = np.expm1(df["price"])

# ----------------------------------------------------------
# Rank Clusters by Average Price
# ----------------------------------------------------------
cluster_price_rank = (
    df.groupby("Cluster")["price_usd"]
    .mean()
    .sort_values()
    .reset_index()
)

print("\nCluster Ranking by Average Price:")
print(cluster_price_rank)

# ----------------------------------------------------------
# Assign Business Segment Labels
# ----------------------------------------------------------
segment_labels = [
    "Budget Segment",
    "Mid-Range Segment",
    "Premium Segment",
    "Luxury Segment"
]

cluster_price_rank["Segment"] = segment_labels

# Merge segment names back
df = df.merge(cluster_price_rank[["Cluster", "Segment"]], on="Cluster")

# ----------------------------------------------------------
# Segment Summary
# ----------------------------------------------------------
segment_summary = (
    df.groupby("Segment")
    .agg({
        "price_usd": "mean",
        "carat": "mean",
        "depth": "mean",
        "table": "mean"
    })
    .sort_values("price_usd")
)

print("\nSegment Business Summary:")
print(segment_summary)

segment_summary.to_csv("data/segment_business_summary.csv")

# ----------------------------------------------------------
# Segment Distribution
# ----------------------------------------------------------
plt.figure(figsize=(8,5))
sns.countplot(
    x="Segment",
    data=df,
    order=segment_summary.index
)
plt.xticks(rotation=30)
plt.title("Distribution of Market Segments")
plt.tight_layout()
plt.savefig("plots/segment_distribution.png")
plt.show()

# ----------------------------------------------------------
# Revenue Contribution by Segment
# ----------------------------------------------------------
revenue_analysis = (
    df.groupby("Segment")["price_usd"]
    .sum()
    .sort_values()
)

plt.figure(figsize=(8,5))
revenue_analysis.plot(kind="bar")
plt.title("Revenue Contribution by Segment")
plt.tight_layout()
plt.savefig("plots/segment_revenue.png")
plt.show()

revenue_analysis.to_csv("data/segment_revenue_contribution.csv")

# ----------------------------------------------------------
# Save Final Dataset
# ----------------------------------------------------------
df.to_csv("data/diamonds_final_segmented_business_ready.csv", index=False)

print("\nSTEP 12 COMPLETED SUCCESSFULLY!")
print("=" * 80)