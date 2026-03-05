<h1 align="center">🔗 Container Communication</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Container_Communication-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scope-All_Communication_Types-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Core_DevOps-orange?style=for-the-badge"/>
</p>

---

## 🌐 Overview

In real applications, containers don't work in isolation — they need to communicate:

| Communication Type | Example |
|--------------------|---------|
| Container → Internet | Calling external REST APIs |
| Container → Host Machine | Connecting to a local database |
| Container → Container | Backend API talking to a database container |

---

# 1️⃣ Container → Internet

Containers have internet access by default through the host's network.

## Example: Python App Fetching from an External API

`app.py`

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print("Status:", response.status_code)
print("Data:", response.json())
```

## Running Inside a Container

```bash
docker run -it python:3.10 bash
```

Inside:

```bash
pip install requests
python app.py
```

## Flow

```
Container App
     │
     ▼
Docker Virtual Network
     │
     ▼
Host Machine Network
     │
     ▼
Internet (External API)
     │
     ▼ Response
Container App
```

✔ No extra configuration needed — internet access works out of the box.

---

# 2️⃣ Container → Host Machine

To connect to a service running on your local machine (e.g. a local MySQL), Docker provides a special hostname:

```
host.docker.internal
```

This resolves to the host machine's IP from inside any container.

## Example: Python Connecting to Local MySQL

```python
import mysql.connector

conn = mysql.connector.connect(
    host="host.docker.internal",   # points to your local machine
    user="root",
    password="rootpass",
    database="localdb"
)

print("Connected to local MySQL!")
```

> ✅ Works on macOS and Windows Docker Desktop.
> 🐧 On Linux, use `--add-host=host.docker.internal:host-gateway` in your `docker run` command.

---

# 3️⃣ Container ↔ Container Communication

The most common pattern in microservices. Containers communicate over a **shared Docker network** using container names as hostnames.

---

## Step 1 — Create a Shared Network

```bash
docker network create appnetwork
```

---

## Step 2 — Start the Database Container

```bash
docker run -d \
  --name mysql-db \
  --network appnetwork \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=testdb \
  mysql:8
```

---

## Step 3 — Python App Connects to MySQL by Container Name

`app.py`

```python
import mysql.connector

conn = mysql.connector.connect(
    host="mysql-db",      # container name acts as hostname
    user="root",
    password="rootpass",
    database="testdb"
)

cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print("MySQL Version:", cursor.fetchone())
```

---

## Step 4 — Start the App Container on the Same Network

```bash
docker run -d \
  --name python-app \
  --network appnetwork \
  python:3.10 sleep infinity

docker exec -it python-app bash
pip install mysql-connector-python
python app.py
```

---

## Communication Flow

```
python-app container
        │
        │  (container name = hostname)
        ▼
   appnetwork (Docker internal DNS)
        │
        ▼
  mysql-db container
```

Docker's built-in DNS resolves `mysql-db` to the correct container IP automatically.

---

## ⚠️ Rules for Container Communication

| Rule | Why It Matters |
|------|----------------|
| Both containers must be on the same network | Otherwise DNS resolution fails entirely |
| Always use container names, never IPs | Container IPs change on every restart |
| Only expose ports needed for external access | Internal traffic doesn't need `-p` mapping |
| Use environment variables for credentials | Avoid hardcoding secrets in source code |

---

## 🎯 Real Production Architecture

```
Browser / Client
        │
        ▼
Frontend Container  (port 3000, exposed)
        │  [internal Docker network]
        ▼
Backend API Container  (port 5000, internal only)
        │  [internal Docker network]
        ▼
Database Container  (port 3306, internal only)
        │
        ▼
External API Service  (outbound internet)
```

Only the **frontend** port is exposed to the outside world — everything else communicates internally.

---

<p align="center">
  ✅ Topic Complete — You now understand all three types of Docker container communication
</p>
