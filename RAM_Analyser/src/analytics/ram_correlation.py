import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

print("\n================================================")
print("STEP 4 : RAM + BROWSING CORRELATION ANALYSIS")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# NEW: plots folder
PLOT_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

browse_file = os.path.join(DATA_DIR, "browsing_sessions.csv")
ram_file = os.path.join(DATA_DIR, "ram_log.csv")

output_file = os.path.join(DATA_DIR, "ram_browsing_merged.csv")

print("Browsing file:")
print(browse_file)

print("\nRAM file:")
print(ram_file)

# ------------------------------------------------
# Load datasets
# ------------------------------------------------

browse = pd.read_csv(browse_file)
ram = pd.read_csv(ram_file)

print("\nBrowsing records:", len(browse))
print("RAM records:", len(ram))

browse["timestamp"] = pd.to_datetime(browse["timestamp"])
ram["timestamp"] = pd.to_datetime(ram["timestamp"])

# ------------------------------------------------
# Merge nearest RAM record to browsing event
# ------------------------------------------------

merged = pd.merge_asof(
    browse.sort_values("timestamp"),
    ram.sort_values("timestamp"),
    on="timestamp",
    direction="nearest"
)

print("\nMerged rows:", len(merged))

# ------------------------------------------------
# RAM per session
# ------------------------------------------------

session_ram = merged.groupby("session_id")["ram_used_mb"].mean()

print("\nAverage RAM per session (Top 10):\n")
print(session_ram.head(10))

# ------------------------------------------------
# RAM per dominant category
# ------------------------------------------------

print("\nRAM usage by dominant session category:\n")

category_ram = merged.groupby("dominant_category")["ram_used_mb"].mean().sort_values(ascending=False)

print(category_ram)

# ------------------------------------------------
# RAM vs session complexity
# ------------------------------------------------

complexity_ram = merged.groupby("session_complexity")["ram_used_mb"].mean()

# ------------------------------------------------
# RAM vs pages visited
# ------------------------------------------------

pages_ram = merged.groupby("pages_visited")["ram_used_mb"].mean()

# ------------------------------------------------
# RAM vs unique domains
# ------------------------------------------------

domains_ram = merged.groupby("unique_domains")["ram_used_mb"].mean()

# ------------------------------------------------
# Save merged dataset
# ------------------------------------------------

merged.to_csv(output_file, index=False)

print("\n================================================")
print("MERGED DATASET SAVED")
print("================================================")

print("Output file:")
print(output_file)

# ------------------------------------------------
# Visualization
# ------------------------------------------------

sns.set_style("whitegrid")

print("\nGenerating analytics plots...\n")

# RAM per category
plt.figure(figsize=(10,5))
category_ram.plot(kind="bar")
plt.title("Average RAM Usage by Session Category")
plt.ylabel("RAM (MB)")
plt.tight_layout()

plot_path = os.path.join(PLOT_DIR, "ram_by_category.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

# RAM vs complexity
plt.figure(figsize=(10,5))
plt.scatter(merged["session_complexity"], merged["ram_used_mb"], alpha=0.5)
plt.title("Session Complexity vs RAM Usage")
plt.xlabel("Session Complexity")
plt.ylabel("RAM (MB)")
plt.tight_layout()

plot_path = os.path.join(PLOT_DIR, "ram_vs_complexity.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

# RAM vs pages
plt.figure(figsize=(10,5))
plt.scatter(merged["pages_visited"], merged["ram_used_mb"], alpha=0.5)
plt.title("Pages Visited vs RAM Usage")
plt.xlabel("Pages Visited")
plt.ylabel("RAM (MB)")
plt.tight_layout()

plot_path = os.path.join(PLOT_DIR, "ram_vs_pages.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

# RAM vs domains
plt.figure(figsize=(10,5))
plt.scatter(merged["unique_domains"], merged["ram_used_mb"], alpha=0.5)
plt.title("Unique Domains vs RAM Usage")
plt.xlabel("Unique Domains")
plt.ylabel("RAM (MB)")
plt.tight_layout()

plot_path = os.path.join(PLOT_DIR, "ram_vs_domains.png")
plt.savefig(plot_path)
print("Saved:", plot_path)

plt.show()
plt.close()

print("\nPlots saved in:", PLOT_DIR)

print("\n================================================")
print("STEP 4 COMPLETED")
print("================================================")