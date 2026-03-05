import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

print("\n================================================")
print("STEP 6 : SESSION CLUSTERING")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# NEW: plot folder
PLOT_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

input_file = os.path.join(DATA_DIR, "session_features.csv")
output_file = os.path.join(DATA_DIR, "session_clusters.csv")

print("Input file:")
print(input_file)

# ------------------------------------------------
# Load dataset
# ------------------------------------------------

df = pd.read_csv(input_file)

print("\nRows loaded:", len(df))

# ------------------------------------------------
# Select features for clustering
# ------------------------------------------------

features = df[[
    "session_length",
    "pages_visited",
    "unique_domains",
    "domain_switches",
    "session_complexity",
    "ram_per_page",
    "session_intensity"
]]

# ------------------------------------------------
# Feature scaling
# ------------------------------------------------

scaler = StandardScaler()
X = scaler.fit_transform(features)

print("\nFeature scaling completed")

# ------------------------------------------------
# KMeans clustering
# ------------------------------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X)

df["cluster"] = clusters

print("\nClusters created:", df["cluster"].nunique())

# ------------------------------------------------
# Silhouette score
# ------------------------------------------------

score = silhouette_score(X, clusters)

print("\nSilhouette Score:", score)

# ------------------------------------------------
# Cluster summary
# ------------------------------------------------

summary = df.groupby("cluster").mean()

print("\nCluster Summary:\n")
print(summary)

# ------------------------------------------------
# Save dataset
# ------------------------------------------------

df.to_csv(output_file, index=False)

print("\n================================================")
print("CLUSTER DATASET SAVED")
print("================================================")

print("Output file:")
print(output_file)

print("\nColumns:")
print(df.columns.tolist())

# ------------------------------------------------
# Visualization
# ------------------------------------------------

sns.set_style("whitegrid")

print("\nGenerating cluster visualizations...\n")

# ------------------------------------------------
# Session Length vs Pages Visited
# ------------------------------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    x=df["session_length"],
    y=df["pages_visited"],
    hue=df["cluster"],
    palette="Set2"
)

plt.title("Browsing Session Clusters")
plt.xlabel("Session Length")
plt.ylabel("Pages Visited")

plt.tight_layout()

# SAVE PLOT
plot_path = os.path.join(PLOT_DIR, "cluster_session_length_vs_pages.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

# ------------------------------------------------
# RAM Efficiency vs Pages Visited
# ------------------------------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    x=df["ram_per_page"],
    y=df["pages_visited"],
    hue=df["cluster"],
    palette="Set1"
)

plt.title("RAM Efficiency vs Browsing Activity")
plt.xlabel("RAM per Page")
plt.ylabel("Pages Visited")

plt.tight_layout()

# SAVE PLOT
plot_path = os.path.join(PLOT_DIR, "cluster_ram_efficiency.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

# ------------------------------------------------
# PCA Cluster Visualization (Professional ML view)
# ------------------------------------------------

print("\nGenerating PCA cluster visualization...\n")

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X)

plt.figure(figsize=(8,6))

sns.scatterplot(
    x=X_pca[:,0],
    y=X_pca[:,1],
    hue=df["cluster"],
    palette="Set2"
)

plt.title("Cluster Visualization (PCA Projection)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")

plt.tight_layout()

# SAVE PLOT
plot_path = os.path.join(PLOT_DIR, "cluster_pca_visualization.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

print("\n================================================")
print("STEP 6 COMPLETED")
print("================================================")