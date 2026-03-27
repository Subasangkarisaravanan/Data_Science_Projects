import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

print("\nSTEP 6 : CLUSTERING")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

df = pd.read_csv(os.path.join(DATA_DIR, "session_features.csv"))

features = df[[
    "session_length",
    "pages_visited",
    "unique_domains",
    "domain_switches",
    "session_complexity",
    "ram_per_page",
    "session_intensity"
]]

X = StandardScaler().fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X)

print("Silhouette:", silhouette_score(X, df["cluster"]))

summary = df.groupby("cluster").mean()

# ------------------------------------------------
# 🔥 AUTO LABELING
# ------------------------------------------------

labels = {}

for cid, row in summary.iterrows():

    if row["session_length"] > 3000:
        labels[cid] = "Heavy Multitasking"
    elif row["session_length"] > 1000:
        labels[cid] = "Focused Work"
    else:
        labels[cid] = "Casual Browsing"

df["cluster_label"] = df["cluster"].map(labels)

print("\nCluster Labels:", labels)

df.to_csv(os.path.join(DATA_DIR, "session_clusters.csv"), index=False)

print("\nSTEP 6 UPDATED")