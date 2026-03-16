# Docker Compose & YAML

## What is Docker Compose?

Docker Compose is a tool that lets you define and run multi-container Docker applications using a single declarative YAML file.

Instead of executing multiple `docker run` commands manually, you describe your entire application stack in one file and launch everything with a single command.

---

## Why Docker Compose is Essential

| Without Compose | With Compose |
|-----------------|--------------|
| Run each container manually | One command starts everything |
| Manually configure networks | Networks created automatically |
| Volumes set up separately | Volumes declared in one file |
| Hard to reproduce for teammates | `docker compose up` anywhere = same result |
| Complex to manage in CI/CD | Single file works in any pipeline |

---

## YAML Basics

Docker Compose uses `docker-compose.yml` written in YAML.

**YAML rules:**
- Uses indentation (2 spaces — never tabs)
- Key-value structure
- Lists use a `-` prefix

```yaml
app_name: my-application
version: "1.0"
tags:
  - backend
  - production
```

---

## Full `docker-compose.yml` Structure

```yaml
version: "3.9"

services:
  service_name:
    image: image_name
    build: .
    container_name: my-container
    ports:
      - "host_port:container_port"
    volumes:
      - volume_name:/container_path
    environment:
      - KEY=value
    env_file:
      - .env
    networks:
      - mynetwork
    depends_on:
      - other_service
    restart: always

networks:
  mynetwork:

volumes:
  volume_name:
```

---

## Example 1 — Single Container (Nginx)

```yaml
version: "3.9"

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

```bash
docker compose up
# Open: http://localhost:8080
```

---

## Example 2 — Full Stack App (Python + MySQL)

```yaml
version: "3.9"

services:
  db:
    image: mysql:8
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
    volumes:
      - dbdata:/var/lib/mysql
    networks:
      - appnetwork
    restart: always

  app:
    build: .
    container_name: python-app
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - appnetwork
    restart: on-failure

networks:
  appnetwork:

volumes:
  dbdata:
```

---

## Key Compose Fields Reference

| Key | Purpose |
|-----|---------|
| `version` | Compose file format version |
| `services` | Define all container services |
| `image` | Use an existing Docker image |
| `build` | Build image from a local Dockerfile |
| `container_name` | Assign a fixed name to the container |
| `ports` | Map `host:container` ports |
| `volumes` | Mount named volumes or bind mounts |
| `environment` | Set environment variables inline |
| `env_file` | Load variables from a `.env` file |
| `networks` | Connect service to named networks |
| `depends_on` | Define startup dependency order |
| `restart` | Restart policy on failure or exit |

---

## Restart Policies

```yaml
restart: always          # Always restart on any exit
restart: on-failure      # Restart only on non-zero exit codes
restart: unless-stopped  # Restart unless manually stopped
restart: "no"            # Never restart (default)
```

---

## Using `.env` with Compose

Store all secrets and configuration in a `.env` file:

```env
DB_PASSWORD=mysecretpass
DB_NAME=appdb
APP_PORT=5000
```

Reference in `docker-compose.yml`:

```yaml
environment:
  MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
  MYSQL_DATABASE: ${DB_NAME}
ports:
  - "${APP_PORT}:5000"
```

> Always add `.env` to `.gitignore` — never commit secrets to version control.

---

## Docker Compose Commands

| Command | Purpose |
|---------|---------|
| `docker compose up` | Start all services |
| `docker compose up -d` | Start in background (detached) |
| `docker compose down` | Stop and remove containers and networks |
| `docker compose down -v` | Also remove named volumes |
| `docker compose build` | Build or rebuild service images |
| `docker compose ps` | List running services |
| `docker compose logs` | View logs from all services |
| `docker compose logs app` | View logs from one specific service |
| `docker compose restart` | Restart all services |
| `docker compose stop` | Stop without removing containers |
| `docker compose exec app bash` | Enter a running service container |
| `docker compose pull` | Pull latest images for all services |

---

## When to Use Docker Compose

- Running backend, database, and cache together locally
- Standardizing development environments across a team
- Testing multi-service interactions before deployment
- Powering CI/CD pipeline service dependencies
