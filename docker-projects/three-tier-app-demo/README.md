```markdown
# Three-Tier Application

A production-style web application built with Flask, MySQL, and Nginx —
fully containerized and orchestrated with Docker Compose.

---

## Architecture

```
User → Nginx :3000 → Flask :5000 → MySQL :3307
```

---

## Project Structure

```
three-tier-app-demo/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   └── Dockerfile
└── docker-compose.yml
```

---

## Backend Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Frontend Dockerfile

```dockerfile
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY index.html /usr/share/nginx/html/index.html

RUN echo 'server { \
  listen 80; \
  root /usr/share/nginx/html; \
  index index.html; \
  location / { try_files $uri $uri/ /index.html; } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
```

## requirements.txt

```text
flask
flask-cors
pymysql
cryptography
```

## docker-compose.yml

```yaml
version: "3.8"

services:

  mysqldb:
    image: mysql:8
    container_name: mysqldb
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: testdb
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app-network

  backend:
    build: ./backend
    container_name: flask-backend
    restart: always
    environment:
      DB_HOST: mysqldb
      DB_USER: root
      DB_PASSWORD: root
      DB_NAME: testdb
    ports:
      - "5000:5000"
    depends_on:
      - mysqldb
    networks:
      - app-network

  frontend:
    build: ./frontend
    container_name: nginx-frontend
    restart: always
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - app-network

volumes:
  mysql_data:

networks:
  app-network:
    driver: bridge
```

---

## Quick Start

```bash
# Build and start all services
docker-compose up --build

# Run in the background
docker-compose up -d

# Stop everything
docker-compose down
```

---

## Endpoints

| Service      | URL                             |
|--------------|---------------------------------|
| Frontend     | http://localhost:3000           |
| Backend      | http://localhost:5000           |
| Health Check | http://localhost:5000/health    |
| Stats        | http://localhost:5000/api/stats |
| Users        | http://localhost:5000/api/users |

---

## Database Access

```bash
# Connect to the MySQL container
docker exec -it mysqldb mysql -u root -p
```

```sql
-- Select database and query users
USE testdb;
SELECT * FROM users;

-- Insert a record
INSERT INTO users (name, email, role)
VALUES ('Shubham Mali', 'shubham@gmail.com', 'admin');
```

---

## Features

- Three-tier separation of concerns across Frontend, Backend, and Database
- Single-command startup with Docker Compose
- MySQL data persistence via named volumes
- Automatic schema creation and seed data on first run
- REST API with Flask and CORS support
- Health check endpoint for monitoring
- Nginx serving the dashboard on port 3000
```
