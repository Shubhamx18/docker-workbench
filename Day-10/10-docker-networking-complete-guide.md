<h1 align="center">🌐 Day 10 – Docker Networking (Complete & Clear Guide)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Docker_Networking-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Container_Communication-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Core_DevOps-orange?style=for-the-badge"/>
</p>

---

# ❓ What is Docker Networking?

Docker Networking is the system that allows **containers to communicate** with:

✔ Other containers  
✔ The host machine  
✔ The internet  

When Docker runs a container, it automatically connects it to a virtual network so it can send and receive data.

---

# 🎯 Why Do We Need Docker Networks?

Real-world applications are made of multiple services:

```
Frontend → Backend API → Database → External APIs
```

Each service runs in a separate container.  
Docker networking connects them so they can talk to each other.

Without Docker networking, containers would be isolated and unable to communicate.

---

# 🧠 How Docker Networking Works

Each container gets:

- A unique IP address  
- A virtual network interface  
- Access to Docker’s internal DNS  

Docker creates a virtual network bridge between containers and manages routing.

---

# 🚦 Types of Docker Network Drivers

| Network Type | Purpose |
|--------------|---------|
| **bridge** | Default network for containers |
| **host** | Container uses host’s network directly |
| **none** | No network access |
| **overlay** | Multi-host communication (Swarm) |
| **macvlan** | Container gets its own MAC address |

---

## 🏗 1️⃣ Bridge Network (Default)

Docker automatically creates a **bridge network** named `bridge`.

Check networks:

```bash
docker network ls
```

Run a container:

```bash
docker run -d nginx
```

This connects it to the default bridge network.

⚠ Containers on default bridge cannot easily resolve each other by name.

---

## 🌟 2️⃣ Custom Bridge Network (Recommended)

Creating your own network is best practice.

### ➕ Create a Network

```bash
docker network create mynetwork
```

### ▶ Run Containers on This Network

```bash
docker run -d --name app --network mynetwork nginx
docker run -d --name db --network mynetwork mysql
```

Now containers can communicate using names:

```
app → db
```

Docker provides automatic DNS resolution.

---

## 🌍 3️⃣ Host Network

Container shares host’s network.

```bash
docker run --network host nginx
```

✔ No port mapping needed  
❌ No isolation from host  

Used for performance-sensitive applications.

---

## 🚫 4️⃣ None Network

Container has no network access.

```bash
docker run --network none ubuntu
```

Used for security or testing.

---

## 🌐 5️⃣ Overlay Network

Used when containers run on multiple Docker hosts (Docker Swarm).

```bash
docker network create -d overlay myoverlay
```

---

# 🔌 Port Mapping (Expose Container to Host)

```bash
docker run -d -p 8080:80 nginx
```

| Host Port | Container Port |
|-----------|----------------|
| 8080 | 80 |

Access app in browser:

```
http://localhost:8080
```

---

# 🔎 Inspect a Network

```bash
docker network inspect mynetwork
```

Shows:
- Connected containers  
- IP addresses  
- Network details  

---

# ➕ Connect a Running Container to a Network

```bash
docker network connect mynetwork container_name
```

Disconnect:

```bash
docker network disconnect mynetwork container_name
```

---

# 🧠 Docker Internal DNS

Inside a custom network, Docker allows containers to use **container names as hostnames**.

Example:

```python
host="mysql-db"
```

No need to know IP addresses.

---

# 🔄 Real Communication Flow

```
Frontend Container
        ↓
Backend API Container
        ↓
Database Container
```

All containers connected via a custom Docker network.

---

# 🎯 Best Practices

✔ Use custom bridge networks  
✔ Use container names instead of IPs  
✔ Only expose required ports  
✔ Keep services on separate networks for security  
✔ Avoid using host network unless necessary  

---

# 🏁 Summary

Docker networking allows containers to communicate with each other, the host, and the internet.

We learned:

✔ What Docker networks are  
✔ Why they are needed  
✔ How to create and use networks  
✔ Types of network drivers  
✔ Port mapping and DNS resolution  

Networking is the backbone of multi-container applications in DevOps.

---

<p align="center">
  ✅ Day 10 Complete – You now clearly understand Docker Networking
</p>
