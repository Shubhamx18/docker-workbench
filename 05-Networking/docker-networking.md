<h1 align="center">🌐 Docker Networking</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Docker_Networking-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Network_Drivers-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Core_DevOps-orange?style=for-the-badge"/>
</p>

---

## ❓ What is Docker Networking?

Docker Networking is the built-in system that allows containers to communicate with:

✔ Other containers on the same host
✔ The host machine
✔ External internet services

When Docker starts a container, it automatically connects it to a virtual network so it can send and receive data.

---

## 🎯 Why Networking is Essential

Real-world applications are multi-service:

```
Frontend Container
      │
      ▼
Backend API Container
      │
      ▼
Database Container
      │
      ▼
External API / Services
```

Without Docker networking, these containers cannot find or talk to each other.

---

## 🧠 How Docker Networking Works

Each container on a Docker network receives:
- A **unique IP address** on the virtual network
- A **virtual network interface**
- Access to **Docker's internal DNS** for name resolution

---

## 🚦 Network Driver Types

| Driver | Purpose | Use Case |
|--------|---------|----------|
| `bridge` | Default isolated network on single host | Most container workloads |
| `host` | Container shares host's network stack | Performance-critical apps |
| `none` | No network access at all | Batch jobs, security testing |
| `overlay` | Spans multiple Docker hosts | Docker Swarm clusters |
| `macvlan` | Container gets its own MAC address | Legacy network integration |

---

## 🏗 Bridge Network (Default)

Docker automatically creates a default network called `bridge`:

```bash
# View all existing networks
docker network ls

# Run a container (connects to default bridge automatically)
docker run -d nginx
```

> ⚠️ Containers on the **default** bridge network **cannot resolve each other by name** — always create a custom network instead.

---

## 🌟 Custom Bridge Network (Recommended)

Creating a named custom network is DevOps best practice:

```bash
# Create a custom network
docker network create mynetwork

# Run containers on this network
docker run -d --name frontend --network mynetwork nginx
docker run -d --name backend --network mynetwork my-api
docker run -d --name database --network mynetwork mysql

# "frontend" can now reach "backend" and "database" by name
```

Docker provides **automatic DNS resolution** — container names are used as hostnames directly.

---

## 🌍 Host Network

The container shares the host machine's full network stack:

```bash
docker run --network host nginx
```

✔ No port mapping required
✔ Best performance for network-heavy apps
❌ No network isolation from the host

---

## 🚫 None Network

Completely disables all networking for a container:

```bash
docker run --network none ubuntu
```

Used for security isolation or standalone batch processing.

---

## 🌐 Overlay Network (Docker Swarm)

Enables communication between containers running across **multiple Docker hosts**:

```bash
docker network create -d overlay cluster-network
```

Required for Docker Swarm multi-host deployments.

---

## 🔌 Port Mapping

Expose a container's port to the host machine:

```bash
docker run -d -p 8080:80 nginx
```

| Host Port | Container Port | Browser Access |
|-----------|----------------|----------------|
| 8080 | 80 | `http://localhost:8080` |
| 5432 | 5432 | PostgreSQL on host port 5432 |
| 3000 | 3000 | Node.js app on port 3000 |

> Internal container-to-container traffic does **not** need port mapping.

---

## 🔎 Network Management Commands

```bash
# List all networks
docker network ls

# Create a custom network
docker network create mynetwork

# Inspect a network (see connected containers, IPs)
docker network inspect mynetwork

# Connect a running container to a network
docker network connect mynetwork container_name

# Disconnect a container from a network
docker network disconnect mynetwork container_name

# Remove a network
docker network rm mynetwork

# Remove all unused networks
docker network prune
```

---

## 🧠 Docker Internal DNS

Inside a custom network, Docker acts as an internal DNS server — **container names resolve to their IP addresses automatically**.

```bash
# You can ping containers by name
docker exec frontend ping backend
docker exec frontend curl http://backend:5000/api
```

No need to hardcode IPs — they change on every restart anyway.

---

## 🎯 Networking Best Practices

✔ Always use **custom bridge networks** — never rely on the default
✔ Use **container names** as hostnames — never hardcode IPs
✔ Only expose ports that need **external** access
✔ Use **separate networks** to isolate frontend from database
✔ Avoid `--network host` unless you have a specific performance need

---

<p align="center">
  ✅ Topic Complete — You now understand all Docker network drivers, port mapping, and DNS resolution
</p>
