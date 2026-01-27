<h1 align="center">🔗 Day 9 – Container Communication (Complete Guide)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Container_Communication-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scope-Networking_&_APIs-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Important-orange?style=for-the-badge"/>
</p>

---

# 🌐 Why Container Communication Matters

Modern applications are made of multiple services:

- Backend API 🧠  
- Database 🗄  
- Frontend 🌍  
- External APIs 🌐  

All these services must communicate properly for the system to work.

---

# 📚 Types of Container Communication

| Type | Example |
|------|---------|
| Container → Internet | Calling external APIs |
| Container → Local Machine | Accessing local database |
| Container → Container | Backend talking to database |

---

# 1️⃣ Container → Internet (Fetching Data from Web API)

Containers can access the internet by default using the host network.

## 📝 Python Example (`app.py`)

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print("Status Code:", response.status_code)
print("Response Data:", response.json())
```

---

## 🐳 Run This Inside a Docker Container

```bash
docker run -it python:3.10 bash
```

Inside the container:

```bash
pip install requests
nano app.py
```

Paste the Python code and run:

```bash
python app.py
```

---

### 📡 What Happens Here?

```
Python App (inside container)
        ↓
Docker Network
        ↓
Internet API Server
        ↓
Response sent back to container
```

✔ Containers can access external APIs  
✔ No special network setup needed  

---

# 2️⃣ Container → Local Machine Communication

Sometimes containers must connect to services running on the host machine (like a local database).

Docker provides a special hostname:

```
host.docker.internal
```

### Example Python DB Connection

```python
import mysql.connector

conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="rootpass",
    database="localdb"
)
```

This allows the container to communicate with services on your local system.

---

# 3️⃣ Container ↔ Container Communication

This is the most common communication method in microservices.

Containers talk using **Docker Networks**.

---

## 🧱 Step 1 – Create a Custom Network

```bash
docker network create mynetwork
```

---

## 🗄 Step 2 – Run MySQL Container

```bash
docker run -d \
  --name mysql-db \
  --network mynetwork \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=testdb \
  mysql:8
```

---

## 🐍 Step 3 – Python App Connecting to MySQL

```python
import mysql.connector

conn = mysql.connector.connect(
    host="mysql-db",
    user="root",
    password="rootpass",
    database="testdb"
)

print("Connected to MySQL!")
```

Here, `mysql-db` is the container name used as host.

---

## 🚀 Step 4 – Run Python Container

```bash
docker run -d \
  --name python-app \
  --network mynetwork \
  python:3.10 sleep infinity
```

Then:

```bash
docker exec -it python-app bash
pip install mysql-connector-python
python app.py
```

---

## 🔄 Communication Flow

```
Python Container → Docker Network → MySQL Container
```

Docker provides automatic DNS resolution for container names.

---

# ⚠️ Important Rules

| Rule | Explanation |
|------|-------------|
| Containers must be on same network | Otherwise they cannot communicate |
| Use container names instead of IPs | IPs can change |
| Expose ports only for external access | Not needed internally |
| Use environment variables for credentials | Secure configuration |

---

# 🎯 Real DevOps Scenario

```
Frontend Container → Backend API Container → Database Container
Backend Container → External API Service
```

This is how real cloud-native applications are structured.

---

# 🏁 Summary

Today we covered all important container communication types:

✔ Container accessing the Internet (APIs)  
✔ Container connecting to services on the local machine  
✔ Container-to-container communication using Docker networks  

These concepts are essential for multi-container applications and DevOps environments.

---

<p align="center">
  ✅ Day 9 Complete – You now understand real-world Docker communication
</p>
