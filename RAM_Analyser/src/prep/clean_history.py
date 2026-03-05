import pandas as pd
import os
import tldextract

print("\n================================================")
print("STEP 2 : DATA PREPROCESSING")
print("================================================\n")

# ------------------------------------------------
# Project paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

history_file = os.path.join(DATA_DIR, "browsing_history_raw.csv")
category_file = os.path.join(DATA_DIR, "domain_category_map.csv")

output_file = os.path.join(DATA_DIR, "browsing_history_clean.csv")

print("Input file:")
print(history_file)

# ------------------------------------------------
# Load browsing history
# ------------------------------------------------

df = pd.read_csv(history_file)

print("\nRows loaded:", len(df))

# ------------------------------------------------
# Remove query strings (privacy rule)
# ------------------------------------------------

df["url"] = df["url"].astype(str).str.split("?").str[0]

# ------------------------------------------------
# Extract domain
# ------------------------------------------------

def extract_domain(url):
    try:
        ext = tldextract.extract(url)
        domain = ext.domain + "." + ext.suffix
        return domain.lower()
    except:
        return "unknown"

df["domain"] = df["url"].apply(extract_domain)

print("Domain extraction completed")

# ------------------------------------------------
# Load domain category mapping
# ------------------------------------------------

category_map = pd.read_csv(category_file)

category_map["domain"] = category_map["domain"].str.lower()

domain_dict = dict(zip(category_map["domain"], category_map["category"]))

# ------------------------------------------------
# Map category
# ------------------------------------------------

def map_category(domain):

    # exact match
    if domain in domain_dict:
        return domain_dict[domain]

    # try root domain fallback
    parts = domain.split(".")
    if len(parts) > 2:
        root = ".".join(parts[-2:])
        if root in domain_dict:
            return domain_dict[root]

    return "other"


df["category"] = df["domain"].apply(map_category)

print("Domain → category mapping completed")

# ------------------------------------------------
# Timestamp processing
# ------------------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["weekday"] = df["timestamp"].dt.day_name()

print("Time features created")

# ------------------------------------------------
# Remove duplicates
# ------------------------------------------------

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("Duplicates removed:", before - after)

# ------------------------------------------------
# Top domain analytics
# ------------------------------------------------

print("\nTop 10 domains:\n")

print(df["domain"].value_counts().head(10))

# ------------------------------------------------
# Category analytics
# ------------------------------------------------

print("\nCategory distribution:\n")

print(df["category"].value_counts())

# ------------------------------------------------
# Hourly browsing pattern
# ------------------------------------------------

print("\nHourly browsing distribution:\n")

print(df["hour"].value_counts().sort_index())

# ------------------------------------------------
# Daily browsing pattern
# ------------------------------------------------

print("\nWeekday browsing distribution:\n")

print(df["weekday"].value_counts())

# ------------------------------------------------
# Save cleaned dataset
# ------------------------------------------------

df.to_csv(output_file, index=False)

print("\n================================================")
print("CLEAN DATASET SAVED")
print("================================================")

print("Output file:")
print(output_file)

print("\nFinal rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nSample rows:\n")

print(df.head(10))

print("\n================================================")
print("STEP 2 COMPLETED")
print("================================================")