<h1 align="center">🐳 Day 12 – Docker Commands Complete Cheat Sheet</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Docker-Commands-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Level-DevOps_Ready-success?style=for-the-badge"/>
</p>

This guide contains the most important Docker commands used in real DevOps workflows.

---

# 📦 IMAGE COMMANDS

| Command | Description |
|--------|-------------|
| `docker images` | List images |
| `docker pull image` | Download image |
| `docker build -t name .` | Build image from Dockerfile |
| `docker tag image newname` | Tag an image |
| `docker rmi image` | Remove image |
| `docker history image` | Show image layers |

---

# 🚀 CONTAINER COMMANDS

| Command | Description |
|--------|-------------|
| `docker run image` | Run container |
| `docker run -d image` | Run in background |
| `docker run -it image` | Interactive mode |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop id` | Stop container |
| `docker start id` | Start container |
| `docker restart id` | Restart container |
| `docker rm id` | Remove container |
| `docker logs id` | View logs |
| `docker exec -it id bash` | Enter container |

---

# 🌐 NETWORK COMMANDS

| Command | Description |
|--------|-------------|
| `docker network ls` | List networks |
| `docker network create name` | Create network |
| `docker network inspect name` | Inspect network |
| `docker network connect net container` | Connect container |
| `docker network disconnect net container` | Disconnect container |
| `docker network rm name` | Remove network |

---

# 💾 VOLUME COMMANDS

| Command | Description |
|--------|-------------|
| `docker volume ls` | List volumes |
| `docker volume create name` | Create volume |
| `docker volume inspect name` | Inspect volume |
| `docker volume rm name` | Remove volume |

---

# 🔍 SYSTEM & CLEANUP COMMANDS

| Command | Description |
|--------|-------------|
| `docker info` | System info |
| `docker version` | Docker version |
| `docker stats` | Container resource usage |
| `docker system df` | Disk usage |
| `docker system prune` | Remove unused data |
| `docker system prune -a` | Remove unused images |
| `docker container prune` | Remove stopped containers |
| `docker image prune` | Remove unused images |
| `docker volume prune` | Remove unused volumes |
| `docker network prune` | Remove unused networks |

---

# 🧱 DOCKERFILE & BUILD COMMANDS

| Command | Description |
|--------|-------------|
| `docker build .` | Build image |
| `docker build -f Dockerfile.dev .` | Use specific Dockerfile |
| `docker commit container image` | Save container as image |

---

# 🌍 DOCKER HUB / REGISTRY

| Command | Description |
|--------|-------------|
| `docker login` | Login to Docker Hub |
| `docker logout` | Logout |
| `docker push image` | Upload image |
| `docker pull image` | Download image |

---

# ⚙️ DOCKER COMPOSE COMMANDS

| Command | Description |
|--------|-------------|
| `docker compose up` | Start services |
| `docker compose up -d` | Start in background |
| `docker compose down` | Stop and remove |
| `docker compose build` | Build services |
| `docker compose ps` | List services |
| `docker compose logs` | View logs |
| `docker compose exec service bash` | Enter service container |

---

# 🧠 PRO TIPS

✔ Use `--help` with any command  
✔ Use `docker ps -q` to get only IDs  
✔ Combine prune commands carefully in production  

---

<p align="center">
  🎉 Congratulations! You now have a complete practical understanding of Docker commands used in DevOps.
</p>
