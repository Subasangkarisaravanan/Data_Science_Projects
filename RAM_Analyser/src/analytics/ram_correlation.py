import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from src.config.paths import SESSION_HISTORY

print("\n================================================")
print("STEP 4 : ADVANCED RAM CORRELATION ANALYSIS")
print("================================================\n")

# ------------------------------------------------
# Load Data
# ------------------------------------------------

if not os.path.exists(SESSION_HISTORY):
    print("❌ File not found:", SESSION_HISTORY)
    exit()

browse = pd.read_csv(SESSION_HISTORY)

if browse.empty:
    print("⚠️ No data available")
    exit()

print(f"📊 Rows loaded: {len(browse)}")

# ------------------------------------------------
# Convert timestamp
# ------------------------------------------------

browse["timestamp"] = pd.to_datetime(browse["timestamp"], errors="coerce")
browse.dropna(subset=["timestamp"], inplace=True)

browse["hour"] = browse["timestamp"].dt.hour

# ------------------------------------------------
# Plot folder
# ------------------------------------------------

PLOT_DIR = os.path.join(os.path.dirname(SESSION_HISTORY), "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

sns.set(style="whitegrid")

# =================================================
# 📊 SESSION SUMMARY (PRINT)
# =================================================

print("\n📊 SESSION SUMMARY:\n")
print(browse[[
    "session_id",
    "session_duration",
    "pages_visited",
    "session_complexity",
    "engagement_level",
    "dominant_category"
]].head(10))

# =================================================
# 📊 CATEGORY ANALYSIS (PRINT)
# =================================================

category_analysis = browse.groupby("category").agg(
    total_visits=("url", "count"),
    avg_duration=("session_duration", "mean"),
    avg_pages=("pages_visited", "mean")
)

print("\n📊 CATEGORY ANALYSIS:\n")
print(category_analysis.sort_values("total_visits", ascending=False))

# =================================================
# 📊 HOURLY ANALYSIS (PRINT)
# =================================================

hourly_analysis = browse.groupby("hour").agg(
    visits=("url", "count"),
    avg_complexity=("session_complexity", "mean")
)

print("\n⏰ HOURLY ACTIVITY:\n")
print(hourly_analysis)

# =================================================
# 🌐 TOP DOMAINS (PRINT)
# =================================================

top_domains = browse["domain"].value_counts().head(10)

print("\n🌐 TOP 10 DOMAINS:\n")
print(top_domains)

# =================================================
# 🔥 ENGAGEMENT DISTRIBUTION (PRINT)
# =================================================

engagement_dist = browse["engagement_level"].value_counts()

print("\n🔥 ENGAGEMENT DISTRIBUTION:\n")
print(engagement_dist)

# =================================================
# 📈 PLOTS SECTION
# =================================================

# 1️⃣ Session Duration
plt.figure(figsize=(8,5))
sns.histplot(browse["session_duration"], bins=40, kde=True, color="skyblue")
plt.axvline(browse["session_duration"].mean(), color="red", linestyle="--")
plt.title("Session Duration Distribution")
plt.savefig(os.path.join(PLOT_DIR, "session_duration.png"))
plt.show()

# 2️⃣ Category Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=browse, x="category", palette="Set2")
plt.title("Category Distribution")
plt.xticks(rotation=30)
plt.savefig(os.path.join(PLOT_DIR, "category_distribution.png"))
plt.show()

# 3️⃣ Hourly Activity
hourly = browse.groupby("hour")["url"].count()

plt.figure(figsize=(10,5))
sns.lineplot(x=hourly.index, y=hourly.values, marker="o", color="purple")
plt.title("Hourly Activity")
plt.savefig(os.path.join(PLOT_DIR, "hourly_activity.png"))
plt.show()

# 4️⃣ Top Domains
plt.figure(figsize=(8,6))
sns.barplot(x=top_domains.values, y=top_domains.index, palette="coolwarm")
plt.title("Top Domains")
plt.savefig(os.path.join(PLOT_DIR, "top_domains.png"))
plt.show()

# 5️⃣ Engagement
plt.figure(figsize=(6,4))
sns.countplot(data=browse, x="engagement_level", palette="viridis")
plt.title("Engagement Levels")
plt.savefig(os.path.join(PLOT_DIR, "engagement.png"))
plt.show()

# 6️⃣ Complexity vs Duration
plt.figure(figsize=(8,5))
sns.scatterplot(
    data=browse,
    x="session_duration",
    y="session_complexity",
    hue="engagement_level",
    palette="Set1"
)
plt.title("Complexity vs Duration")
plt.savefig(os.path.join(PLOT_DIR, "complexity_vs_duration.png"))
plt.show()

# 7️⃣ Category vs Duration
cat_dur = browse.groupby("category")["session_duration"].mean()

plt.figure(figsize=(8,5))
sns.barplot(x=cat_dur.index, y=cat_dur.values, palette="magma")
plt.title("Avg Duration by Category")
plt.xticks(rotation=30)
plt.savefig(os.path.join(PLOT_DIR, "category_duration.png"))
plt.show()

# 8️⃣ Heatmap
heatmap_data = browse.pivot_table(
    index="hour",
    columns="category",
    values="url",
    aggfunc="count",
    fill_value=0
)

plt.figure(figsize=(10,6))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d")
plt.title("Hourly Activity Heatmap")
plt.savefig(os.path.join(PLOT_DIR, "heatmap.png"))
plt.show()

# =================================================
# FINAL SUMMARY PRINT
# =================================================

print("\n================================================")
print("✅ ANALYSIS COMPLETED SUCCESSFULLY")
print("================================================")

print("📁 Plots saved in:", PLOT_DIR)
print("📊 Total sessions:", browse["session_id"].nunique())
print("📊 Avg session duration:", round(browse["session_duration"].mean(), 2), "seconds")
print("🔥 Most common category:", browse["category"].mode()[0])