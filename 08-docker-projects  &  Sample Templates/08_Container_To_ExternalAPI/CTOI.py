import requests
import random

# Cat Facts API endpoint
url = "https://catfact.ninja/facts?limit=50"  # fetch up to 50 facts at once

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    facts = [item['fact'] for item in data.get("data", [])]

    if facts:
        # Pick a random cat fact
        fact = random.choice(facts)
        print("Random Cat Fact:\n")
        print(fact)
    else:
        print("No cat facts found.")
else:
    print("Failed to fetch cat facts. Status code:", response.status_code)
