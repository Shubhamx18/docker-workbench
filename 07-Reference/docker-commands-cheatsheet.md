<h1 align="center">🐳 Docker Commands — Complete Cheat Sheet</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Docker-Commands-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Level-DevOps_Ready-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Type-Quick_Reference-orange?style=for-the-badge"/>
</p>

> A complete reference of every Docker command used in real DevOps workflows — from images to cleanup.

---

## 📦 IMAGE COMMANDS

| Command | Description |
|---------|-------------|
| `docker images` | List all local images |
| `docker pull image:tag` | Download image from registry |
| `docker build -t name:tag .` | Build image from Dockerfile |
| `docker build -f Dockerfile.prod -t name .` | Build from a specific Dockerfile |
| `docker build --build-arg KEY=val .` | Build with a build argument |
| `docker tag image newname:tag` | Tag an existing image |
| `docker rmi image` | Remove an image |
| `docker image prune` | Remove all dangling (unused) images |
| `docker image prune -a` | Remove all unused images |
| `docker history image` | Show image layer history |
| `docker inspect image` | Full image metadata (JSON) |

---

## 🚀 CONTAINER COMMANDS

| Command | Description |
|---------|-------------|
| `docker run image` | Create and start a container |
| `docker run -d image` | Run in background (detached) |
| `docker run -it image bash` | Run with interactive terminal |
| `docker run -p 8080:80 image` | Map host:container port |
| `docker run --name myapp image` | Assign a custom name |
| `docker run --rm image` | Auto-remove container on exit |
| `docker run -e KEY=val image` | Set environment variable |
| `docker run -v vol:/path image` | Mount a volume |
| `docker run --network net image` | Connect to a network |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker ps -q` | List only running container IDs |
| `docker stop id` | Gracefully stop a container |
| `docker start id` | Start a stopped container |
| `docker restart id` | Restart a container |
| `docker rm id` | Remove a stopped container |
| `docker rm -f id` | Force remove (even if running) |
| `docker container prune` | Remove all stopped containers |
| `docker logs id` | View container logs |
| `docker logs -f id` | Follow logs in real-time |
| `docker logs --tail 50 id` | Show last 50 log lines |
| `docker exec -it id bash` | Open shell inside container |
| `docker exec id ls /app` | Run single command in container |
| `docker inspect id` | Full container info (JSON) |
| `docker stats` | Live resource usage (CPU, RAM) |
| `docker top id` | Processes running inside container |
| `docker commit id newimage` | Save container state as new image |

---

## 🌐 NETWORK COMMANDS

| Command | Description |
|---------|-------------|
| `docker network ls` | List all networks |
| `docker network create name` | Create a custom bridge network |
| `docker network create -d overlay name` | Create an overlay network |
| `docker network inspect name` | Inspect network (containers, IPs) |
| `docker network connect net container` | Connect container to network |
| `docker network disconnect net container` | Disconnect container |
| `docker network rm name` | Remove a network |
| `docker network prune` | Remove all unused networks |

---

## 💾 VOLUME COMMANDS

| Command | Description |
|---------|-------------|
| `docker volume ls` | List all volumes |
| `docker volume create name` | Create a named volume |
| `docker volume inspect name` | Inspect a volume (mount path) |
| `docker volume rm name` | Remove a volume |
| `docker volume prune` | Remove all unused volumes |

---

## 🔍 SYSTEM & CLEANUP COMMANDS

| Command | Description |
|---------|-------------|
| `docker info` | System-wide Docker information |
| `docker version` | Docker client and server versions |
| `docker stats` | Live resource usage of all containers |
| `docker system df` | Disk usage by images, containers, volumes |
| `docker system prune` | Remove stopped containers, unused networks, dangling images |
| `docker system prune -a` | Also remove all unused images |
| `docker system prune --volumes` | Also remove unused volumes |

---

## 🌍 DOCKER HUB / REGISTRY COMMANDS

| Command | Description |
|---------|-------------|
| `docker login` | Login to Docker Hub |
| `docker logout` | Logout from Docker Hub |
| `docker push username/image:tag` | Upload image to registry |
| `docker pull username/image:tag` | Download image from registry |
| `docker search term` | Search Docker Hub for images |

---

## ⚙️ DOCKER COMPOSE COMMANDS

| Command | Description |
|---------|-------------|
| `docker compose up` | Start all services |
| `docker compose up -d` | Start all services in background |
| `docker compose down` | Stop and remove containers + networks |
| `docker compose down -v` | Also remove volumes |
| `docker compose build` | Build or rebuild service images |
| `docker compose ps` | List running services |
| `docker compose logs` | View logs from all services |
| `docker compose logs service` | Logs from one specific service |
| `docker compose logs -f` | Follow logs in real-time |
| `docker compose restart` | Restart all services |
| `docker compose stop` | Stop without removing |
| `docker compose exec service bash` | Enter a running service container |
| `docker compose pull` | Pull latest images for services |
| `docker compose config` | Validate and view merged compose file |

---

## 🔧 DOCKERFILE INSTRUCTION REFERENCE

| Instruction | Purpose |
|-------------|---------|
| `FROM image` | Set the base image |
| `WORKDIR /path` | Set working directory |
| `COPY src dest` | Copy files into the image |
| `ADD src dest` | Copy + supports URLs and tar files |
| `RUN command` | Execute during build (creates layer) |
| `CMD ["cmd"]` | Default run command (overridable) |
| `ENTRYPOINT ["cmd"]` | Fixed entry point |
| `EXPOSE port` | Declare the container's port |
| `ENV KEY=value` | Set environment variable |
| `ARG name` | Build-time argument |
| `VOLUME /path` | Declare persistent volume mount point |
| `USER username` | Set the running user |
| `LABEL key=value` | Add image metadata |

---

## 🧠 Power User Tips

```bash
# Stop ALL running containers at once
docker stop $(docker ps -q)

# Remove ALL stopped containers at once
docker rm $(docker ps -aq)

# Remove ALL images at once
docker rmi $(docker images -q)

# Get detailed IP address of a container
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_id

# Copy file from container to host
docker cp container_id:/app/file.txt ./file.txt

# Copy file from host to container
docker cp ./file.txt container_id:/app/file.txt

# Use --help with any command
docker run --help
docker network --help
docker compose up --help
```

---


