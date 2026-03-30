import pandas as pd
from urllib.parse import urlparse, parse_qs
from transformers import pipeline

from src.config.paths import RAW_HISTORY, CLEAN_HISTORY

print("\n================================================")
print("STEP 1 : CLEAN HISTORY WITH AI CATEGORIZATION")
print("================================================\n")

# -------------------------------
# LOAD DATA
# -------------------------------
print(f"Loading file from: {RAW_HISTORY}")

df = pd.read_csv(RAW_HISTORY)
df.dropna(subset=["url"], inplace=True)

# -------------------------------
# LOAD AI MODEL (Better Model)
# -------------------------------
print("Loading AI model...")

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"   # 🔥 More accurate than distilbert
)

CATEGORIES = [
    "Entertainment",
    "Shopping",
    "Social Media",
    "Education",
    "Work",
    "News",
    "Technology",
    "Finance",
    "Gaming",
    "Other"
]

# -------------------------------
# URL CLEANING
# -------------------------------
def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return str(url).lower()


# -------------------------------
# 🔥 SEARCH QUERY EXTRACTION
# -------------------------------
def extract_search_query(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        params = parse_qs(parsed.query)

        if "google" in domain or "bing" in domain or "duckduckgo" in domain:
            return params.get("q", [None])[0]

    except:
        pass

    return None


# -------------------------------
# RULE-BASED LOGIC (STRONG RULES)
# -------------------------------
CATEGORY_MAP = {
    "Entertainment": ["netflix", "hotstar", "primevideo"],
    "Shopping": ["amazon", "flipkart", "meesho"],
    "Social Media": ["facebook", "instagram", "twitter"],
    "Work": ["linkedin", "outlook"],
    "Education": ["coursera", "udemy", "geeksforgeeks"],
    "Technology": ["github", "stackoverflow"],
    "News": ["bbc", "cnn", "ndtv"],
}


def rule_based_category(text):
    text = str(text).lower()

    for category, keywords in CATEGORY_MAP.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return None


# -------------------------------
# AI CATEGORIZATION (WITH CONFIDENCE)
# -------------------------------
def ai_categorize(text):
    try:
        result = classifier(text, CATEGORIES)

        label = result["labels"][0]
        score = result["scores"][0]

        return label, score

    except Exception as e:
        return "Other", 0.0


# -------------------------------
# 🔥 FINAL CATEGORY FUNCTION (IMPROVED)
# -------------------------------
def get_category(url):
    domain = extract_domain(url)

    # Step 1: Extract search query
    query = extract_search_query(url)

    # Step 2: Choose best text
    if query and len(query.strip()) > 2:
        text = query.lower()
    else:
        text = domain

    # Step 3: Strong rule-based first
    rule_cat = rule_based_category(text)
    if rule_cat:
        return rule_cat, 1.0, "Rule"

    # Step 4: AI classification
    ai_cat, score = ai_categorize(text)

    # 🔥 Step 5: Confidence threshold (VERY IMPORTANT)
    if score < 0.4:
        return "Other", score, "LowConfidence"

    return ai_cat, score, "AI"


# -------------------------------
# APPLY (OPTIMIZED)
# -------------------------------
print("Applying categorization...")

results = df["url"].apply(get_category)

df["category"] = results.apply(lambda x: x[0])
df["confidence"] = results.apply(lambda x: x[1])
df["method"] = results.apply(lambda x: x[2])

# -------------------------------
# SAVE
# -------------------------------
df.to_csv(CLEAN_HISTORY, index=False)

print(f"\n✅ Cleaned file saved to: {CLEAN_HISTORY}")
print("================================================\n")