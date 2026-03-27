import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Fix for Windows plot display
import matplotlib
matplotlib.use('TkAgg')

print("\n================================================")
print("STEP 4 : ADVANCED RAM CORRELATION ANALYSIS")
print("================================================\n")

# ------------------------------------------------
# PATHS
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOT_DIR = os.path.join(BASE_DIR, "plots")

os.makedirs(PLOT_DIR, exist_ok=True)

browse = pd.read_csv(os.path.join(DATA_DIR, "browsing_sessions.csv"))
ram = pd.read_csv(os.path.join(DATA_DIR, "ram_log.csv"))

browse["timestamp"] = pd.to_datetime(browse["timestamp"])
ram["timestamp"] = pd.to_datetime(ram["timestamp"])

print("Browsing rows:", len(browse))
print("RAM rows:", len(ram))

# ------------------------------------------------
# SESSION LEVEL RAM
# ------------------------------------------------

session_ram = []

for sid, group in browse.groupby("session_id"):

    start = group["timestamp"].min()

    nearest = ram.iloc[(ram["timestamp"] - start).abs().argsort()[:1]]

    avg_ram = nearest["ram_used_mb"].values[0]

    for _, row in group.iterrows():
        r = row.to_dict()
        r["ram_used_mb"] = avg_ram
        session_ram.append(r)

merged = pd.DataFrame(session_ram)

merged.to_csv(os.path.join(DATA_DIR, "ram_browsing_merged.csv"), index=False)

# ------------------------------------------------
# ROW LEVEL (FOR RICH VISUALS)
# ------------------------------------------------

row_level = pd.merge_asof(
    browse.sort_values("timestamp"),
    ram.sort_values("timestamp"),
    on="timestamp",
    direction="nearest"
)

row_level = row_level.dropna(subset=["ram_used_mb"])

print("Row-level rows:", len(row_level))

# ------------------------------------------------
# PLOT FUNCTION
# ------------------------------------------------

sns.set_style("whitegrid")

def plot_save_show(name):
    path = os.path.join(PLOT_DIR, name)
    plt.tight_layout()
    plt.savefig(path)
    print("Saved:", path)
    plt.show()
    plt.close()

# ------------------------------------------------
# 1. RAM BY CATEGORY
# ------------------------------------------------

plt.figure(figsize=(10,5))
merged.groupby("dominant_category")["ram_used_mb"].mean().plot(kind="bar")
plt.title("RAM Usage by Category")
plot_save_show("ram_by_category.png")

# ------------------------------------------------
# 2. RAM vs COMPLEXITY
# ------------------------------------------------

plt.figure(figsize=(10,5))
plt.scatter(merged["session_complexity"], merged["ram_used_mb"])
plt.title("Session Complexity vs RAM")
plot_save_show("ram_vs_complexity.png")

# ------------------------------------------------
# 3. RAM vs PAGES
# ------------------------------------------------

plt.figure(figsize=(10,5))
plt.scatter(merged["pages_visited"], merged["ram_used_mb"])
plt.title("Pages vs RAM")
plot_save_show("ram_vs_pages.png")

# ------------------------------------------------
# 4. RAM vs DOMAINS
# ------------------------------------------------

plt.figure(figsize=(10,5))
plt.scatter(merged["unique_domains"], merged["ram_used_mb"])
plt.title("Domains vs RAM")
plot_save_show("ram_vs_domains.png")

# ------------------------------------------------
# 5. RAM OVER TIME
# ------------------------------------------------

plt.figure(figsize=(10,5))
plt.plot(row_level["timestamp"], row_level["ram_used_mb"])
plt.title("RAM Usage Over Time")
plot_save_show("ram_over_time.png")

# ------------------------------------------------
# 6. RAM DISTRIBUTION
# ------------------------------------------------

plt.figure(figsize=(10,5))
sns.histplot(row_level["ram_used_mb"], bins=30)
plt.title("RAM Distribution")
plot_save_show("ram_distribution.png")

# ------------------------------------------------
# 7. RAM VS DOMAIN SWITCH
# ------------------------------------------------

plt.figure(figsize=(10,5))
plt.scatter(row_level["domain_switch"], row_level["ram_used_mb"])
plt.title("Domain Switch vs RAM")
plot_save_show("ram_vs_switch.png")

# ------------------------------------------------
# 8. CATEGORY BOXPLOT
# ------------------------------------------------

plt.figure(figsize=(10,5))
sns.boxplot(x="category", y="ram_used_mb", data=row_level)
plt.xticks(rotation=45)
plt.title("RAM by Category Distribution")
plot_save_show("ram_category_boxplot.png")

# ------------------------------------------------
# 9. TOP DOMAINS
# ------------------------------------------------

top_domains = row_level["domain"].value_counts().head(10)

plt.figure(figsize=(10,5))
sns.barplot(x=top_domains.index, y=top_domains.values)
plt.xticks(rotation=45)
plt.title("Top Domains")
plot_save_show("top_domains.png")

# ------------------------------------------------
# 10. RAM vs CPU (if exists)
# ------------------------------------------------

if "cpu_percent" in row_level.columns:
    plt.figure(figsize=(10,5))
    plt.scatter(row_level["cpu_percent"], row_level["ram_used_mb"])
    plt.title("CPU vs RAM")
    plot_save_show("cpu_vs_ram.png")

# ------------------------------------------------
# SAVE ANALYTICS FILES
# ------------------------------------------------

# High RAM sites
merged.groupby("domain")["ram_used_mb"].mean().sort_values(ascending=False)\
.head(10).to_csv(os.path.join(DATA_DIR, "high_ram_sites.csv"))

# Slow sites
merged.groupby("domain")["session_complexity"].mean().sort_values(ascending=False)\
.head(10).to_csv(os.path.join(DATA_DIR, "slow_sites.csv"))

print("\n================================================")
print("ALL ANALYSIS GRAPHS GENERATED SUCCESSFULLY")
print("================================================")