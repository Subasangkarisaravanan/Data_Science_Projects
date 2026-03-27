import pandas as pd
import os

print("\n================================================")
print("STEP 1 : CLEAN HISTORY")
print("================================================\n")

# -------------------------------------------------
# Project paths (same logic as Step 0)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "browsing_history_raw.csv")
OUTPUT_DIR = os.path.join(DATA_DIR, "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cleaned_history.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Input file:", INPUT_FILE)
print("Output file:", OUTPUT_FILE)


# -------------------------------------------------
# CATEGORY FUNCTION
# -------------------------------------------------

def get_category(url):
    if not isinstance(url, str):
        return "Other"

    url = url.lower()

    CATEGORY_MAP = {
        "Entertainment": [
            "netflix", "hotstar", "primevideo", "amazonprime",
            "youtube", "instagram", "facebook", "twitter", "snapchat"
        ],

        "Shopping": [
            "amazon", "flipkart", "meesho", "myntra",
            "zomato", "swiggy", "ajio"
        ],

        "Learning": [
            "coursera", "udemy", "geeksforgeeks",
            "w3schools", "khanacademy", "edx", "byjus", "guvi"
        ],

        "Personal": [
            "gmail", "mail.google", "yahoo",
            "outlook", "drive.google",
            "bank", "netbanking", "upi",
            "paytm", "gpay", "phonepe"
        ],

        "Work": [
            "slack", "teams", "zoom", "meet.google",
            "jira", "confluence"
        ],

        "Search": [
            "google.com/search", "bing.com/search", "yahoo.com/search"
        ]
    }

    for category, keywords in CATEGORY_MAP.items():
        for keyword in keywords:
            if keyword in url:
                return category

    return "Other"


# -------------------------------------------------
# CLEAN FUNCTION
# -------------------------------------------------

def clean_history():

    print("\n📥 Reading raw data...")

    if not os.path.exists(INPUT_FILE):
        print("❌ File not found:", INPUT_FILE)
        return

    df = pd.read_csv(INPUT_FILE)

    print("Total rows:", len(df))

    # ------------------------------
    # BASIC CLEANING
    # ------------------------------

    df.dropna(subset=["timestamp", "url"], inplace=True)

    print("Rows after removing nulls:", len(df))

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    print("Rows after removing duplicates:", len(df))

    # ------------------------------
    # ADD CATEGORY
    # ------------------------------

    print("\n🔍 Categorizing URLs...")

    df["category"] = df["url"].apply(get_category)

    # ------------------------------
    # SORT DATA
    # ------------------------------

    df = df.sort_values("timestamp")

    # ------------------------------
    # SAVE CLEANED DATA
    # ------------------------------

    df.to_csv(OUTPUT_FILE, index=False)

    print("\n================================================")
    print("CLEANING COMPLETED")
    print("================================================")

    print("Saved to:", OUTPUT_FILE)
    print("Final rows:", len(df))

    print("\nCategory distribution:\n")
    print(df["category"].value_counts())


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":
    clean_history()