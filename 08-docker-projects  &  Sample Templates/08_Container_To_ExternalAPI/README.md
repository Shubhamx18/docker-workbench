# Container to External API

## What This Demonstrates

A Docker container can make outbound HTTP requests to the internet by default. No special network configuration is needed. The container uses the host machine's network interface to reach external URLs just like any regular process would.

---

## Project Structure

```
container-to-externalApi/
├── Dockerfile
└── CTOI.py
```

---

## How It Works

```
Container
└── CTOI.py
        |
        | HTTP GET (requests library)
        |
        v
https://catfact.ninja/facts?limit=50
        |
        v
Returns JSON --> picks a random fact --> prints it
```

The container makes a `GET` request to the public Cat Facts API, parses the JSON response, and prints one randomly selected fact. No ports need to be exposed. No host networking flags are needed. Outbound internet access works out of the box.

---

## The Script

```python
import requests
import random

url = "https://catfact.ninja/facts?limit=50"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    facts = [item['fact'] for item in data.get("data", [])]
    if facts:
        fact = random.choice(facts)
        print("Random Cat Fact:\n")
        print(fact)
    else:
        print("No cat facts found.")
else:
    print("Failed to fetch cat facts. Status code:", response.status_code)
```

---

## Dockerfile

```dockerfile
FROM python

WORKDIR /communication

COPY /CTOI.py .

RUN pip install requests

CMD ["python", "CTOI.py"]
```

---

## Build and Run

```bash
# Build the image
docker build -t external-api-app .

# Run the container
docker run external-api-app
```

---

## Expected Output

```
Random Cat Fact:

A cat's jaw can't move sideways, so it can't chew large chunks of food.
```

The fact printed will be different on each run since it is selected randomly from the API response.

---

## Key Point

Docker containers have outbound internet access by default. The container's traffic goes through the host's network interface and out to the internet. You do not need:

- `--network host`
- Any port mapping (`-p`)
- Any firewall rules for outbound traffic

The only requirement is that the host machine itself has internet access.