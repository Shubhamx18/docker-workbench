<h1 align="center">⚙️ Day 11 – Docker Compose & YAML File Guide</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Tool-Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/File-docker--compose.yml-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Concept-Multi_Container_App-orange?style=for-the-badge"/>
</p>

---

# ❓ What is Docker Compose?

Docker Compose is a tool used to **define and run multi-container Docker applications** using a single YAML file.

Instead of running many `docker run` commands, we define everything in **one file** and start all services together.

---

# 🎯 Why Docker Compose is Important

✔ Manage multiple containers easily  
✔ Define networks, volumes, and ports in one place  
✔ Perfect for microservices applications  
✔ Used in DevOps CI/CD workflows  

---

# 📄 What is a YAML File?

Docker Compose uses a **YAML file** (`docker-compose.yml`) to define services.

YAML stands for **YAML Ain’t Markup Language**.

Basic YAML rules:
- Uses **indentation** (spaces, not tabs)
- Key-value structure

Example:

```yaml
name: myapp
version: "1.0"
```

---

# 🧱 Basic Structure of `docker-compose.yml`

```yaml
version: "3.9"

services:
  service_name:
    image: image_name
    ports:
      - "host_port:container_port"
    volumes:
      - volume_name:/container_path
    environment:
      - KEY=value
```

---

# 🐳 Example 1 – Single Container Using Compose

```yaml
version: "3.9"

services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

Run:

```bash
docker compose up
```

---

# 🧩 Example 2 – Multi-Container App (Python + MySQL)

```yaml
version: "3.9"

services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: testdb
    volumes:
      - dbdata:/var/lib/mysql

  app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db

volumes:
  dbdata:
```

---

## 🔍 Important Docker Compose Keys

| Key | Purpose |
|-----|---------|
| `version` | Compose file version |
| `services` | Define containers |
| `image` | Use existing image |
| `build` | Build from Dockerfile |
| `ports` | Port mapping |
| `volumes` | Persistent storage |
| `environment` | Set environment variables |
| `depends_on` | Service startup order |

---

# 🔁 Compose Commands

| Command | Purpose |
|---------|---------|
| `docker compose up` | Start services |
| `docker compose up -d` | Run in background |
| `docker compose down` | Stop and remove containers |
| `docker compose ps` | List services |
| `docker compose logs` | View logs |

---

# 🧠 When Do We Use Compose?

✔ Running backend + database together  
✔ Development environments  
✔ Microservices testing  
✔ DevOps pipelines  

---

# 🎯 Summary

Docker Compose allows us to define multi-container applications using a YAML file and run everything with a single command.

It simplifies networking, volumes, and service management — making it essential for modern DevOps workflows.

---

<p align="center">
  ✅ Day 11 Complete – You now understand Docker Compose and YAML structure
</p>
