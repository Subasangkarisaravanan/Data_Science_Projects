# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 09_clustering.py
# STEP 11 – MARKET SEGMENTATION USING K-MEANS
# ==========================================================

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ----------------------------------------------------------
# Setup folders
# ----------------------------------------------------------
os.makedirs("plots", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 11: MARKET SEGMENTATION (K-MEANS CLUSTERING)")
print("=" * 80)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------
df = pd.read_csv("data/diamonds_step5_feature_engineered.csv")

# ----------------------------------------------------------
# Select Business-Relevant Features
# ----------------------------------------------------------
clustering_features = [
    "carat",
    "depth",
    "table",
    "price"
]

X = df[clustering_features]

# ----------------------------------------------------------
# Scaling
# ----------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "models/clustering_scaler.pkl")

# ----------------------------------------------------------
# Elbow Method
# ----------------------------------------------------------
inertia = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(K_range, inertia, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.tight_layout()
plt.savefig("plots/elbow_method.png")
plt.show()

# ----------------------------------------------------------
# Silhouette Scores
# ----------------------------------------------------------
silhouette_scores = []

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

plt.figure(figsize=(8,5))
plt.plot(K_range, silhouette_scores, marker='o')
plt.title("Silhouette Score vs K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.tight_layout()
plt.savefig("plots/silhouette_scores.png")
plt.show()

# ----------------------------------------------------------
# Choose Optimal K (Based on plots)
# ----------------------------------------------------------
optimal_k = 4   # Adjust after reviewing plots if needed

print(f"\nUsing Optimal K = {optimal_k}")

kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df["Cluster"] = kmeans_final.fit_predict(X_scaled)

# Save model
joblib.dump(kmeans_final, "models/kmeans_model.pkl")

# ----------------------------------------------------------
# Cluster Summary
# ----------------------------------------------------------
cluster_summary = df.groupby("Cluster")[clustering_features].mean()

print("\nCluster Summary:")
print(cluster_summary)

cluster_summary.to_csv("data/cluster_summary.csv")

# ----------------------------------------------------------
# Visualize Clusters (Carat vs Price)
# ----------------------------------------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(
    x="carat",
    y="price",
    hue="Cluster",
    data=df,
    palette="Set2"
)
plt.title("Market Segmentation: Carat vs Price")
plt.tight_layout()
plt.savefig("plots/cluster_visualization.png")
plt.show()

# ----------------------------------------------------------
# Save Segmented Dataset
# ----------------------------------------------------------
df.to_csv("data/diamonds_segmented.csv", index=False)

print("\nSTEP 11 COMPLETED SUCCESSFULLY!")
print("=" * 80)