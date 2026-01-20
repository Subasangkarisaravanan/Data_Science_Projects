import requests

api_key = "bd697abc-1aab-44dc-86b1-4f9d7bab39b1"
base_url = f"https://api.harvardartmuseums.org/classification?apikey={api_key}"

all_classifications = []
page = 1

while True:
    url = f"{base_url}&page={page}"
    response = requests.get(url).json()
    
    all_classifications.extend(response['records'])
    
    # Stop if this is the last page
    if page >= response['info']['pages']:
        break
    page += 1

# Print total classifications and names
print(f"Total classifications: {len(all_classifications)}")
for cls in all_classifications:
    print(cls['name'])
