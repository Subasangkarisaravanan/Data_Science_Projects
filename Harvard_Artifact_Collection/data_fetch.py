import requests

API_KEY = "bd697abc-1aab-44dc-86b1-4f9d7bab39b1"
CLASSIFICATION_URL = "https://api.harvardartmuseums.org/classification"

def get_classifications_over_2500(api_key, min_records=2500):
    classifications = []
    params = {
        "apikey": api_key,
        "size": 100
    }
    url = CLASSIFICATION_URL

    while url:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(url)

        data = response.json()
        for cls in data.get("records", []):
            if cls.get("objectcount", 0) > min_records:
                classifications.append({
                    "id": cls.get("id"),
                    "name": cls.get("name"),
                    "objectcount": cls.get("objectcount")
                })

        next_url = data.get("info", {}).get("next")
        url = f"https://api.harvardartmuseums.org{next_url}" if next_url else None
        params = {}  # already included in next_url

    return classifications

# ==========================
# RUN
# ==========================
results = get_classifications_over_2500(API_KEY)

print(f"\nClassifications with more than 2500 records ({len(results)}):\n")
for cls in results:
    print(f"{cls['name']} — {cls['objectcount']}")