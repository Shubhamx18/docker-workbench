<h1 align="center">Running & Managing Containers</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Container_Management-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Lifecycle_&_Commands-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge"/>
</p>

---

## Running a Container

The `docker run` command creates and starts a container from an image:

```bash
docker run nginx
```

If the image is not available locally, Docker automatically pulls it first.

---

## Common `docker run` Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-d` | Detached mode — run in background | `docker run -d nginx` |
| `-p` | Port mapping (host:container) | `docker run -p 8080:80 nginx` |
| `--name` | Assign a custom name | `docker run --name web nginx` |
| `-it` | Interactive terminal session | `docker run -it ubuntu bash` |
| `--rm` | Auto-remove container on exit | `docker run --rm ubuntu` |
| `-e` | Set environment variable | `docker run -e DB=mydb mysql` |
| `-v` | Mount a volume | `docker run -v mydata:/data nginx` |
| `--network` | Connect to a Docker network | `docker run --network mynet nginx` |

---

## Detached Mode

Run a container in the background so the terminal stays free:

```bash
docker run -d nginx
```

---

## Port Mapping

Expose a container's application to the host machine:

```bash
docker run -d -p 8080:80 nginx
```

| Host Port | Container Port | Access |
|-----------|----------------|--------|
| 8080 | 80 | `http://localhost:8080` |

---

## Naming Containers

```bash
docker run -d --name my-web-server nginx
```

Named containers are much easier to reference than auto-generated IDs.

---

## Running Multiple Containers from the Same Image

```bash
docker run -d -p 8081:80 --name web1 nginx
docker run -d -p 8082:80 --name web2 nginx
docker run -d -p 8083:80 --name web3 nginx
```

Each container runs independently with its own port mapping.

---

## Listing Containers

```bash
# Show only running containers
docker ps

# Show all containers (running + stopped)
docker ps -a

# Show only container IDs
docker ps -q
```

---

## Stopping & Starting

```bash
# Gracefully stop a container
docker stop container_id
docker stop container_name

# Start a stopped container
docker start container_id

# Restart a container
docker restart container_id
```

---

## Removing Containers

```bash
# Remove a stopped container
docker rm container_id

# Force remove a running container
docker rm -f container_id

# Remove all stopped containers at once
docker container prune
```

---

## Viewing Logs

```bash
# View all logs
docker logs container_id

# Follow logs in real-time (like tail -f)
docker logs -f container_id

# Show last 50 lines only
docker logs --tail 50 container_id

# Include timestamps in output
docker logs --timestamps container_id
```

---

## Executing Commands Inside a Running Container

```bash
# Open an interactive bash shell
docker exec -it container_id bash

# Run a single one-off command
docker exec container_id ls /app

# Run as a specific user
docker exec -u root -it container_id bash
```

---

## Inspecting Containers

```bash
# Full JSON details — IP, mounts, network, environment variables
docker inspect container_id

# Live resource usage — CPU, memory, network I/O
docker stats

# Processes running inside a specific container
docker top container_id
```

---

## Container Lifecycle

```
docker run
     │
     ▼
  Running ──── docker stop ────▶ Stopped
     │                               │
     │                        docker start
     │                               │
     ◀──────────────────────────────┘
     │
docker rm
     │
     ▼
  Removed
```

---

## Why Container Management Matters in DevOps

- Monitor live applications and track resource usage in real time
- Quickly restart failed or unresponsive containers
- Debug issues by accessing container logs and interactive shells
- Scale services by running multiple independent container instances
- Clean up stale containers to free system resources
