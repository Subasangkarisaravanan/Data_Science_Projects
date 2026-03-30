import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src.config.paths import DATA_DIR  # ✅ central path

print("\n================================================")
print("STEP 6 : SESSION CLUSTERING (ENHANCED)")
print("================================================\n")

# ------------------------------------------------
# PATHS (FIXED)
# ------------------------------------------------

input_file = os.path.join(DATA_DIR, "processed", "session_features.csv")
output_file = os.path.join(DATA_DIR, "processed", "session_clusters.csv")

print("📥 Input:", input_file)
print("📤 Output:", output_file)

# ------------------------------------------------
# FILE CHECK
# ------------------------------------------------

if not os.path.exists(input_file):
    print("❌ File not found:", input_file)
    exit()

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = pd.read_csv(input_file)

if df.empty:
    print("⚠️ No data available")
    exit()

print(f"📊 Rows loaded: {len(df)}")

# ------------------------------------------------
# SELECT FEATURES
# ------------------------------------------------

feature_cols = [
    "session_length",
    "pages_visited",
    "unique_domains",
    "domain_switches",
    "session_complexity",
    "ram_per_page",
    "session_intensity"
]

# Ensure columns exist
feature_cols = [col for col in feature_cols if col in df.columns]

features = df[feature_cols].fillna(0)

print("\n📋 Features used:", feature_cols)

# ------------------------------------------------
# SCALING
# ------------------------------------------------

scaler = StandardScaler()
X = scaler.fit_transform(features)

# ------------------------------------------------
# 🔥 AUTO FIND BEST K (IMPORTANT)
# ------------------------------------------------

best_k = 2
best_score = -1

print("\n🔍 Finding optimal clusters...\n")

for k in range(2, 6):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X)

    score = silhouette_score(X, labels)
    print(f"K={k} → Silhouette Score={round(score, 4)}")

    if score > best_score:
        best_k = k
        best_score = score

print(f"\n✅ Best K selected: {best_k}")

# ------------------------------------------------
# FINAL MODEL
# ------------------------------------------------

kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

print("\n📊 Final Silhouette Score:", round(best_score, 4))

# ------------------------------------------------
# CLUSTER SUMMARY
# ------------------------------------------------

summary = df.groupby("cluster")[feature_cols].mean()

print("\n📊 CLUSTER SUMMARY:\n")
print(summary)

# ------------------------------------------------
# 🔥 AUTO LABELING (IMPROVED)
# ------------------------------------------------

labels = {}

for cid, row in summary.iterrows():

    if row["session_length"] > 3000 and row["session_complexity"] > 50:
        labels[cid] = "Heavy Multitasking"

    elif row["session_length"] > 1000:
        labels[cid] = "Focused Work"

    elif row["pages_visited"] > 20:
        labels[cid] = "Exploratory Browsing"

    else:
        labels[cid] = "Casual Browsing"

df["cluster_label"] = df["cluster"].map(labels)

print("\n🏷️ Cluster Labels:\n", labels)

# ------------------------------------------------
# DISTRIBUTION
# ------------------------------------------------

print("\n📊 Cluster Distribution:\n")
print(df["cluster_label"].value_counts())

# ------------------------------------------------
# SAVE
# ------------------------------------------------

os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)

print("\n================================================")
print("✅ CLUSTERING COMPLETED")
print("================================================")

print("📁 Saved to:", output_file)