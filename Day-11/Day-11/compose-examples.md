<h1 align="center">🧩 Docker Compose Examples – From Basic to Advanced</h1>

This file contains practical `docker-compose.yml` examples covering single-container, multi-container, and advanced DevOps setups.

---

# 🟢 1️⃣ Simple Compose File (Single Container)

```yaml
version: "3.9"

services:
  web:
    image: nginx:latest
    container_name: my_nginx
    ports:
      - "8080:80"     # Host:Container
    restart: always
```

### ▶ Run

```bash
docker compose up -d
```

This runs a single Nginx container and exposes it on port **8080**.

---

# 🟡 2️⃣ Multi-Container App (App + Database)

```yaml
version: "3.9"

services:
  app:
    build: .
    container_name: python_app
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: rootpass
    depends_on:
      - db
    networks:
      - appnet

  db:
    image: mysql:8
    container_name: mysql_db
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: testdb
    volumes:
      - dbdata:/var/lib/mysql
    networks:
      - appnet

volumes:
  dbdata:

networks:
  appnet:
```

### 🔍 What This Shows

✔ Containers communicate using service name **`db`**  
✔ Volume **dbdata** stores database data permanently  
✔ Custom network **appnet** isolates the application  

---

# 🔴 3️⃣ Advanced Compose File (All Important Concepts)

```yaml
version: "3.9"

services:

  frontend:
    image: nginx:latest
    container_name: frontend_service
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - frontend_net

  backend:
    build: ./backend
    container_name: backend_service
    ports:
      - "5000:5000"
    environment:
      DB_HOST: database
      DB_USER: root
      DB_PASSWORD: rootpass
    volumes:
      - ./backend:/app           # Bind mount (local folder)
    depends_on:
      - database
    networks:
      - frontend_net
      - backend_net
    restart: unless-stopped

  database:
    image: mysql:8
    container_name: mysql_service
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: appdb
    volumes:
      - dbdata:/var/lib/mysql    # Named volume
    networks:
      - backend_net
    restart: always

volumes:
  dbdata:   # Named volume

networks:
  frontend_net:
  backend_net:
```

### 🔍 Concepts Covered

| Feature | Purpose |
|--------|---------|
| `image` | Pull images from Docker Hub |
| `build` | Build image from Dockerfile |
| `ports` | Expose services to host |
| `environment` | Pass configuration to containers |
| `volumes (named)` | Persistent database storage |
| `volumes (bind)` | Sync local code into container |
| `depends_on` | Control service startup order |
| `networks` | Secure container communication |
| `restart` | Automatically restart containers |

---

<p align="center">
  🚀 These examples demonstrate real-world Docker Compose usage in DevOps
</p>
