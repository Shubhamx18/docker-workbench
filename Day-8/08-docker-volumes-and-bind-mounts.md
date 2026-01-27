<h1 align="center">💾 Day 8 – Docker Volumes & Bind Mounts (Data Persistence)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Data_Persistence-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Storage-Docker_Volumes-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Mounts-Bind_Mounts-orange?style=for-the-badge"/>
</p>

---

## ❓ Why Do We Need Data Persistence in Docker?

By default, containers are **temporary**.

If a container is deleted, all data inside it is lost ❌

Example:  
If a database runs inside a container and the container is removed, all stored data disappears.

To solve this, Docker provides **Volumes** and **Bind Mounts**.

---

# 📦 What is a Docker Volume?

A **Docker Volume** is a special storage area managed by Docker that stores data **outside the container’s writable layer**.

Even if the container stops or is removed, the data remains safe.

### 🧠 Purpose of Volumes

✔ Store database data  
✔ Keep application files safe  
✔ Share data between containers  
✔ Maintain persistent logs  

---

## 🛠 How to Create a Volume

```bash
docker volume create myvolume
```

Check volumes:

```bash
docker volume ls
```

Inspect a volume:

```bash
docker volume inspect myvolume
```

---

## 🔗 How to Use a Volume in a Container

```bash
docker run -d -v myvolume:/data ubuntu
```

Explanation:

| Part | Meaning |
|------|---------|
| `-v` | Mount volume |
| `myvolume` | Docker volume name |
| `/data` | Path inside container |

Now anything stored in `/data` is saved in the volume.

---

## 🗑 Remove a Volume

```bash
docker volume rm myvolume
```

---

# 📂 What is a Bind Mount?

A **Bind Mount** connects a specific folder from your local system directly into a container.

Instead of Docker managing storage, you choose the folder.

---

## 🧠 Purpose of Bind Mounts

✔ Share source code during development  
✔ Access container files from host  
✔ Live editing of project files  
✔ Debugging and testing  

---

## 🔗 How to Use Bind Mount (Local Folder → Container)

```bash
docker run -d -v /home/user/project:/app nginx
```

Explanation:

| Part | Meaning |
|------|---------|
| `/home/user/project` | Local folder on host machine |
| `/app` | Folder inside container |

Changes in local folder reflect inside container instantly.

---

## 📊 Volume vs Bind Mount (Comparison)

| Feature | Docker Volume | Bind Mount |
|---------|---------------|------------|
| Managed by | Docker | User |
| Location | Docker storage path | Any local path |
| Best for | Databases, production data | Development work |
| Easy to share between containers | Yes | Not ideal |
| Depends on host structure | No | Yes |

---

## 🔄 Real-World Examples

### 🗄 Database Container with Volume

```bash
docker run -d -v dbdata:/var/lib/mysql mysql
```

MySQL data remains safe even if container stops.

---

### 💻 Development with Bind Mount

```bash
docker run -d -v $(pwd):/app node-app
```

Your local code syncs with the container.

---

# 🚫 What is `.dockerignore`?

`.dockerignore` tells Docker which files to **exclude while building an image**.

It helps keep images small and secure.

---

## 📝 Example `.dockerignore`

```
node_modules
.git
.env
__pycache__
*.log
```

---

## 🎯 Why `.dockerignore` is Important

✔ Reduces image size  
✔ Improves build speed  
✔ Avoids leaking secrets  
✔ Keeps builds clean  

---

# 🧠 DevOps Perspective

| Scenario | Use Volume | Use Bind Mount |
|----------|------------|----------------|
| Production database | ✅ | ❌ |
| Development code sync | ❌ | ✅ |
| Shared persistent storage | ✅ | ❌ |
| Testing & debugging | ❌ | ✅ |

---

## 🏁 Summary

Today we learned:

✔ Why containers lose data by default  
✔ How Docker Volumes store persistent data  
✔ How Bind Mounts link local folders to containers  
✔ When to use each storage type  
✔ How `.dockerignore` keeps images optimized  

These are essential for running real-world containerized applications.

---

<p align="center">
  ✅ Day 8 Complete – You now understand Docker data persistence
</p>
