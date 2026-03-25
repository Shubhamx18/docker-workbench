```markdown
# Three-Tier Application
## What This Demonstrates
A Docker Compose setup that runs three containers together — Nginx, Flask, and MySQL —
each isolated in its own container but connected through a shared internal network.
The browser talks to Nginx, Nginx talks to Flask, and Flask talks to MySQL.
No direct database exposure. No manual networking. Just one command.

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

## How It Works
```
Browser
└── http://localhost:3000
        |
        | HTTP (port 3000)
        |
        v
Nginx Container (frontend)
        |
        | Proxy / static serve
        |
        v
Flask Container (backend) :5000
        |
        | pymysql
        |
        v
MySQL Container (mysqldb) :3306
        |
        v
Returns data --> Flask formats JSON --> Nginx delivers to browser
```

All three containers share `app-network` defined in Docker Compose.
MySQL is never exposed to the browser directly. Flask is the only service
that talks to the database.

---

## The Backend

### backend/app.py
```python
from flask import Flask, jsonify
from flask_cors import CORS
import pymysql, os, time, datetime

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "mysqldb"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "testdb"),
    "connect_timeout": 5
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def wait_for_db():
    retries = 0
    while retries < 15:
        try:
            get_connection().close()
            print("Connected to MySQL")
            return
        except Exception as e:
            retries += 1
            print(f"Waiting for MySQL... ({retries}): {e}")
            time.sleep(3)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100), email VARCHAR(100),
            role VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)", [
            ("Alice Johnson", "alice@example.com", "admin"),
            ("Bob Smith",     "bob@example.com",   "developer"),
            ("Carol White",   "carol@example.com", "developer"),
            ("Dave Brown",    "dave@example.com",  "viewer"),
            ("Eve Davis",     "eve@example.com",   "viewer"),
        ])
        conn.commit()
    cursor.close()
    conn.close()

@app.route("/health")
def health():
    try:
        get_connection().close()
        db = "connected"
    except:
        db = "disconnected"
    return jsonify({"status": "healthy", "database": db,
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z"})

@app.route("/api/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users ORDER BY id")
    users = cursor.fetchall()
    for u in users:
        if u.get("created_at"):
            u["created_at"] = str(u["created_at"])
    cursor.close()
    conn.close()
    return jsonify({"users": users, "count": len(users)})

@app.route("/api/stats")
def stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    roles = {r[0]: r[1] for r in cursor.fetchall()}
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify({"total_users": total, "roles": roles,
                    "db_version": version, "db_name": DB_CONFIG["database"]})

if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
```

### backend/requirements.txt
```text
flask
flask-cors
pymysql
cryptography
```

### backend/Dockerfile
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

---

## The Frontend

### frontend/Dockerfile
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

---

## Docker Compose
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

## Build and Run
```bash
# Build all images and start containers
docker-compose up --build

# Run in the background
docker-compose up -d

# Stop and remove containers
docker-compose down
```

---

## Expected Output
```
flask-backend  | Waiting for MySQL... (1)
flask-backend  | Connected to MySQL
flask-backend  | Seed data inserted
flask-backend  | Running on http://0.0.0.0:5000
```

Visit `http://localhost:3000` in the browser. The dashboard loads,
fetches live data from Flask, and renders the user table and service health status.

---

## Endpoints
```
GET  http://localhost:5000/health      → service and database status
GET  http://localhost:5000/api/users   → all users from MySQL
GET  http://localhost:5000/api/stats   → totals, roles, DB version
```

---

## Database Access
```bash
# Open a MySQL shell inside the container
docker exec -it mysqldb mysql -u root -p
```
```sql
USE testdb;
SELECT * FROM users;

INSERT INTO users (name, email, role)
VALUES ('Shubham Mali', 'shubham@gmail.com', 'admin');
```

---

## Key Point
Docker Compose handles all networking automatically. Containers talk to each other
using their service name as the hostname — Flask connects to MySQL simply by using
`mysqldb` as the host. You do not need to:
- hardcode IP addresses
- expose MySQL to the host machine
- configure any manual DNS

The only port the browser ever touches is `3000`. Everything behind it stays internal.
```
