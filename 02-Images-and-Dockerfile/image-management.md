<h1 align="center">Docker Image Management</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Image_Management-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Tags_&_Layers-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Mode-Interactive_Containers-orange?style=for-the-badge"/>
</p>

---

## What is a Docker Image?

A **Docker Image** is a read-only, layered template used to create containers.

It contains:
- Application source code
- All runtime dependencies
- Libraries and system tools
- Environment configuration

> **Image = Blueprint** | **Container = Running instance of the blueprint**

---

## Image Commands Reference

```bash
# List all images on your system
docker images

# Pull an image from Docker Hub
docker pull nginx:latest
docker pull python:3.10-slim

# Build an image from a Dockerfile
docker build -t my-app:v1 .

# Remove an image
docker rmi image_id

# Remove all unused images
docker image prune

# View image layer history
docker history image_name

# Detailed image metadata
docker inspect image_name
```

---

## Tagging Images

Tags let you manage and version different variants of the same image.

```bash
# Tag format: username/image-name:version
docker tag my-app shubham/my-app:v1
docker tag my-app shubham/my-app:v2
docker tag my-app shubham/my-app:latest
```

| Tag | Meaning |
|-----|---------|
| `v1`, `v2` | Specific version releases |
| `latest` | Most recent build (default if no tag specified) |
| `prod`, `dev` | Environment-specific variants |
| `1.0.0` | Semantic versioning |

> Avoid relying on `latest` in production — always use explicit version tags.

---

## Making Changes Inside a Running Container

For testing or debugging, you can enter a container and modify it manually.

**Step 1:** Start an interactive container

```bash
docker run -it ubuntu /bin/bash
```

**Step 2:** Make changes inside

```bash
apt update && apt install curl -y
```

**Step 3:** Exit

```bash
exit
```

---

## Saving a Modified Container as a New Image

After making changes inside a container, you can snapshot it as a new image:

```bash
docker commit container_id shubham/my-ubuntu:v2
```

> Use `docker commit` for testing only. For production, always define changes in a **Dockerfile** for reproducibility.

---

## Common Base Images

Docker Hub provides official, trusted base images for most use cases:

| Image | Use Case | Size |
|-------|----------|------|
| `ubuntu` | General Linux environment | ~75 MB |
| `alpine` | Minimal Linux (security-focused) | ~5 MB |
| `node:18-alpine` | Node.js apps | ~50 MB |
| `python:3.10-slim` | Python apps | ~45 MB |
| `nginx:alpine` | Web server | ~20 MB |
| `mysql:8` | MySQL database | ~450 MB |
| `postgres:15-alpine` | PostgreSQL database | ~80 MB |

```bash
# Pull a specific base image
docker pull python:3.10-slim
```

---

## Interactive Mode

Interactive mode opens a live terminal session inside a container — useful for testing and debugging.

```bash
docker run -it ubuntu bash
docker run -it python:3.10 bash
```

| Flag | Meaning |
|------|---------|
| `-i` | Keep STDIN open (interactive) |
| `-t` | Allocate a pseudo-terminal |

### When to Use Interactive Mode

| Use Case | Reason |
|----------|--------|
| Testing commands | Try things out safely inside a container |
| Debugging issues | Inspect files, logs, and configs manually |
| Exploring base images | Discover what tools are pre-installed |
| Learning Linux | Practice commands without affecting your host |

> Production containers always run in **detached mode** (`-d`). Interactive mode is for development and debugging only.

---

## Interactive Mode in Docker Compose

```yaml
version: "3.9"

services:
  debug-shell:
    image: ubuntu
    container_name: ubuntu_shell
    stdin_open: true    # equivalent to -i
    tty: true           # equivalent to -t
```

| YAML Key | CLI Equivalent | Purpose |
|----------|----------------|---------|
| `stdin_open: true` | `-i` | Keeps STDIN open |
| `tty: true` | `-t` | Allocates a terminal |

```bash
docker compose up -d
docker exec -it ubuntu_shell bash
```

---

## Image Lifecycle

```
Pull / Build
     │
     ▼
Local Image Store
     │
     ├─── docker run ──────▶ Container
     │
     ├─── docker tag ──────▶ New Name/Version
     │
     ├─── docker push ─────▶ Registry
     │
     └─── docker rmi ──────▶ Deleted
```

---

## Image Management in DevOps

DevOps engineers regularly need to:

- Build and version images per release
- Optimize image size for faster deployments
- Rebuild images when application code changes
- Use trusted, minimal base images to reduce attack surface
