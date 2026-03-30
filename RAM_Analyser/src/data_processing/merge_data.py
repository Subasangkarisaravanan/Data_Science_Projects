import pandas as pd
from src.config.paths import CLEAN_HISTORY, RAM_LOG, MERGED_DATA

print("\n========== MERGING DATA ==========\n")

# Load data
try:
    history_df = pd.read_csv(CLEAN_HISTORY)
    ram_df = pd.read_csv(RAM_LOG)
except Exception as e:
    print("Error loading files:", e)
    exit()

# Ensure timestamp format
history_df["timestamp"] = pd.to_datetime(history_df["timestamp"], errors="coerce")
ram_df["timestamp"] = pd.to_datetime(ram_df["timestamp"], errors="coerce")

# Drop null timestamps
history_df.dropna(subset=["timestamp"], inplace=True)
ram_df.dropna(subset=["timestamp"], inplace=True)

# Sort for merge_asof
history_df.sort_values("timestamp", inplace=True)
ram_df.sort_values("timestamp", inplace=True)

# Merge (nearest timestamp match)
merged_df = pd.merge_asof(
    history_df,
    ram_df,
    on="timestamp",
    direction="nearest"
)

# Save output
merged_df.to_csv(MERGED_DATA, index=False)

print(f"\n✅ Merged data saved to: {MERGED_DATA}")
print("\n========== DONE ==========\n")