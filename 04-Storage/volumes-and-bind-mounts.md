<h1 align="center">💾 Volumes, Bind Mounts & Data Persistence</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Data_Persistence-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Storage-Docker_Volumes-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Mounts-Bind_Mounts-orange?style=for-the-badge"/>
</p>

---

## ❓ Why Data Persistence is Needed

By default, containers are **stateless and ephemeral**.

When a container is stopped and removed, all data inside it is permanently lost ❌

> **Example:** A MySQL database running inside a container loses all its records the moment the container is deleted — unless persistence is configured.

Docker provides two solutions: **Volumes** and **Bind Mounts**.

---

# 📦 Docker Volumes

A **Docker Volume** is a storage area managed entirely by Docker, stored outside the container's writable layer on the host filesystem.

Data in a volume **persists** even if the container is stopped, removed, or rebuilt.

---

## 🧠 What Volumes Are Used For

✔ Storing database data (MySQL, PostgreSQL, MongoDB)
✔ Persisting application files and uploads
✔ Sharing data between multiple containers
✔ Maintaining logs across container restarts

---

## 🛠 Volume Commands

```bash
# Create a named volume
docker volume create myvolume

# List all volumes
docker volume ls

# Inspect a volume (shows mount path)
docker volume inspect myvolume

# Remove a specific volume
docker volume rm myvolume

# Remove all unused volumes
docker volume prune
```

---

## 🔗 Mounting a Volume to a Container

```bash
docker run -d -v myvolume:/data ubuntu
```

| Part | Meaning |
|------|---------|
| `-v` | Volume mount flag |
| `myvolume` | Named Docker volume |
| `/data` | Mount path inside the container |

Anything written to `/data` inside the container is stored in `myvolume` and persists forever.

---

## 🗄 Real Example — MySQL with Persistent Volume

```bash
docker run -d \
  --name mysql-db \
  -v dbdata:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=appdb \
  mysql:8
```

Even after `docker rm mysql-db`, all database records survive in `dbdata`.

---

# 📂 Bind Mounts

A **Bind Mount** links a specific folder from your local machine directly into the container.

Instead of Docker managing the storage location, **you choose the exact host path**.

---

## 🧠 What Bind Mounts Are Used For

✔ Live code sync during development (no rebuild needed)
✔ Accessing container output files from the host
✔ Mounting configuration files into containers
✔ Debugging by reading container files directly

---

## 🔗 Using a Bind Mount

```bash
docker run -d -v /home/shubham/project:/app nginx
```

| Part | Meaning |
|------|---------|
| `/home/shubham/project` | Absolute path on your host machine |
| `/app` | Target path inside the container |

Changes in your local folder are **instantly reflected** inside the container.

---

## 💻 Development Workflow with Bind Mount

```bash
# Mount current working directory into the container
docker run -d -v $(pwd):/app node-app
```

Edit files locally → changes appear in the container immediately — **no rebuild required**.

---

## 📊 Volumes vs Bind Mounts

| Feature | Docker Volume | Bind Mount |
|---------|---------------|------------|
| Managed by | Docker | You (the user) |
| Storage location | Docker-internal path | Any host path you choose |
| Best for | Databases, production data | Development code sync |
| Share between containers | ✅ Easy | ❌ Not ideal |
| Depends on host structure | No | Yes |
| Backup support | ✅ Built-in with `docker cp` | ❌ Manual |
| Portability | High | Low (host path varies) |

---

## 🧠 DevOps Decision Guide

| Scenario | Use Volume | Use Bind Mount |
|----------|:----------:|:--------------:|
| Production database | ✅ | ❌ |
| Development code sync | ❌ | ✅ |
| Shared storage between containers | ✅ | ❌ |
| Config file injection | ❌ | ✅ |
| Persistent logs | ✅ | ❌ |
| Debugging / testing | ❌ | ✅ |

---

# 🚫 `.dockerignore`

`.dockerignore` tells Docker which files and folders to **exclude when building an image** — similar to `.gitignore`.

---

## 📝 Example `.dockerignore`

```
node_modules/
.git/
.env
__pycache__/
*.log
*.md
dist/
.DS_Store
tests/
```

---

## 🎯 Why `.dockerignore` Matters

✔ Reduces image size (no dev dependencies or logs)
✔ Speeds up the build by sending less context to the daemon
✔ Prevents secrets (`.env`) from leaking into images
✔ Keeps the final image clean and production-ready

---

<p align="center">
  ✅ Topic Complete — You now understand Docker data persistence with Volumes, Bind Mounts, and .dockerignore
</p>
