
# 🐳 Docker Workbench

![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![DevOps](https://img.shields.io/badge/DevOps-Ready-brightgreen?style=for-the-badge)
![Topics](https://img.shields.io/badge/Topics-7_Modules-blue?style=for-the-badge)
![Files](https://img.shields.io/badge/Files-11_Notes-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A complete hands-on Docker learning repository covering containerization, image optimization, networking, volumes, and real-world deployment workflows.

</div>

---

## 📁 Repository Structure

```
docker-workbench/
│
├── 📂 01-Basics/
│   ├── what-is-docker.md
│   ├── containers-and-architecture.md
│   └── docker-vs-virtual-machines.md
│
├── 📂 02-Images-and-Dockerfile/
│   ├── dockerfile-fundamentals.md
│   ├── image-management.md
│   └── docker-hub-registry.md
│
├── 📂 03-Container-Management/
│   └── running-and-managing-containers.md
│
├── 📂 04-Storage/
│   └── volumes-and-bind-mounts.md
│
├── 📂 05-Networking/
│   ├── docker-networking.md
│   └── container-communication.md
│
├── 📂 06-Compose/
│   └── docker-compose-yaml.md
│
└── 📂 07-Reference/
    └── docker-commands-cheatsheet.md
```

---

## 🗂 Module Index

### 📂 01-Basics
| File | Description |
|------|-------------|
| `what-is-docker.md` | What Docker is, problems it solves, real-world workflow, image vs container |
| `containers-and-architecture.md` | Docker Client-Daemon-Host architecture, component breakdown |
| `docker-vs-virtual-machines.md` | VM vs container comparison, core building blocks (Dockerfile, Image, Container, Registry) |

---

### 📂 02-Images-and-Dockerfile
| File | Description |
|------|-------------|
| `dockerfile-fundamentals.md` | All Dockerfile instructions, CMD vs ENTRYPOINT, multi-stage builds, security best practices |
| `image-management.md` | Listing, tagging, removing images, interactive mode, base image selection |
| `docker-hub-registry.md` | Tagging conventions, full push/pull workflow, registry types, sharing images |

---

### 📂 03-Container-Management
| File | Description |
|------|-------------|
| `running-and-managing-containers.md` | `docker run` flags, detached mode, port mapping, logs, exec, inspect, lifecycle |

---

### 📂 04-Storage
| File | Description |
|------|-------------|
| `volumes-and-bind-mounts.md` | Named volumes, bind mounts, when to use each, `.dockerignore` |

---

### 📂 05-Networking
| File | Description |
|------|-------------|
| `docker-networking.md` | Network drivers (bridge, host, none, overlay), port mapping, DNS, best practices |
| `container-communication.md` | Container→Internet, Container→Host, Container↔Container with real examples |

---

### 📂 06-Compose
| File | Description |
|------|-------------|
| `docker-compose-yaml.md` | YAML structure, single & multi-container examples, `.env` usage, restart policies, all Compose commands |

---

### 📂 07-Reference
| File | Description |
|------|-------------|
| `docker-commands-cheatsheet.md` | Complete command reference — images, containers, networks, volumes, Compose, system, registry, power tips |

---

## 🛠 Topics Covered

| Category | Topics |
|----------|--------|
| 🐳 **Basics** | What is Docker, Containerization concept, Docker vs VM |
| 🏗 **Architecture** | Client, Daemon, Host, Registry, Image, Container |
| 📝 **Dockerfile** | All instructions, multi-stage builds, caching, security |
| 🧱 **Images** | Build, tag, commit, push, pull, manage versions |
| 🚀 **Containers** | Run, stop, logs, exec, inspect, lifecycle management |
| 💾 **Storage** | Named volumes, bind mounts, `.dockerignore` |
| 🌐 **Networking** | Bridge, host, overlay, DNS, port mapping |
| 🔗 **Communication** | Container↔Internet, Container↔Host, Container↔Container |
| ⚙️ **Compose** | Multi-container apps, YAML, `.env`, restart policies |
| 📋 **Reference** | Full cheat sheet for all Docker commands |

---

## 🚀 Getting Started

### Prerequisites

- [ ] [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [ ] A [Docker Hub](https://hub.docker.com/) account
- [ ] Basic terminal knowledge

### Clone the Repository

```bash
git clone https://github.com/Shubhamx18/docker-workbench.git
cd docker-workbench
```

### Verify Docker Installation

```bash
docker --version
docker run hello-world
```

---

## 📚 Resources

| Resource | Link |
|----------|------|
| 📖 Docker Docs | [docs.docker.com](https://docs.docker.com/) |
| 🌐 Docker Hub | [hub.docker.com](https://hub.docker.com/) |
| 🔧 Docker Compose Docs | [docs.docker.com/compose](https://docs.docker.com/compose/) |
| 🎓 Docker Getting Started | [docs.docker.com/get-started](https://docs.docker.com/get-started/) |

---

## 🔒 Security Note

> ⚠️ Never commit `.env` files, credentials, `.pem` keys, or registry passwords to this repository.

```bash
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
```

---

## 👤 Author

<div align="center">

**Shubham**
[![GitHub](https://img.shields.io/badge/GitHub-Shubhamx18-181717?style=for-the-badge&logo=github)](https://github.com/Shubhamx18)

*Learning Docker one container at a time 🐳*

⭐ **Star this repo if it helped you!** ⭐

</div>
>>>>>>> 412f1317f6d203d8c442e13e261c78b64e478a9c
