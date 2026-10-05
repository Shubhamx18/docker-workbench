# Flask MySQL App — Production-Grade Containerized Web App

## What This Demonstrates

A full-featured Flask web application connecting to a local MySQL database using a **connection pool** (`dbutils.PooledDB`) and served by **Gunicorn** as a production WSGI server. This is a step up from the basic Flask setup — it uses proper connection management, input validation, and multiple API endpoints including CSV export.

---

## Project Structure

```
flask_mysql_app/
└── app/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

---

## Key Differences from Basic Flask Setup

| Feature | Basic Flask | This App |
|---|---|---|
| DB connection | Single `pymysql.connect()` per request | Connection pool (`PooledDB`) |
| Server | Flask dev server | Gunicorn (production WSGI) |
| Input validation | Minimal | Dedicated `validate_name()` function |
| Export | None | CSV download endpoint |
| Sorting | None | Sort by ID, name, date |
| Bulk operations | None | Bulk delete, reorder |

---

## Database Connection — Connection Pool

Instead of opening and closing a new database connection on every request, this app creates a **pool** of reusable connections at startup:

```python
from dbutils.pooled_db import PooledDB
import pymysql

db_config = {
    'host': "host.docker.internal",   # local MySQL on the host machine
    'user': "appuser",
    'password': "Shubham@6024",
    'database': "hello",
    'cursorclass': pymysql.cursors.DictCursor
}

pool = PooledDB(creator=pymysql, mincached=2, maxcached=10, **db_config)
```

`mincached=2` keeps 2 connections open at all times. `maxcached=10` allows up to 10. Each request borrows a connection from the pool and returns it when done — much faster and more efficient than creating a new connection per request.

The host is `host.docker.internal` which resolves to the host machine's IP from inside the container. This is how the container reaches the locally installed MySQL.

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS test_table (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

Migrations for `sort_order` and `updated_at` columns run automatically on startup if they are missing from an older schema.

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Main UI — list all users with sort options |
| `POST` | `/add` | Add a new user |
| `DELETE` | `/delete/<id>` | Delete a single user by ID |
| `POST` | `/delete-bulk` | Delete multiple users by ID list |
| `PUT` | `/edit/<id>` | Edit an existing user's name |
| `POST` | `/reorder` | Update sort order of entries |
| `GET` | `/search` | Search users by name |
| `GET` | `/stats` | Return aggregate statistics |
| `GET` | `/export` | Download all users as a CSV file |

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

`gcc` and `default-libmysqlclient-dev` are system packages required to compile some MySQL client dependencies. The `requirements.txt` is copied and installed before the rest of the code — this takes advantage of Docker's layer caching so that dependencies are not reinstalled on every code change.

---

## requirements.txt

```
Flask
pymysql
dbutils
gunicorn
```

---

## Prerequisites on Host Machine

MySQL must be running locally with the required database and user:

```sql
CREATE DATABASE hello;
CREATE USER 'appuser'@'%' IDENTIFIED BY 'Shubham@6024';
GRANT ALL PRIVILEGES ON hello.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
```

---

## Build and Run

```bash
cd flask_mysql_app/app

# Build the image
docker build -t flask-mysql-app .

# Run — macOS / Windows
docker run -d -p 5000:5000 flask-mysql-app

# Run — Linux (requires host-gateway flag)
docker run -d -p 5000:5000 --add-host=host.docker.internal:host-gateway flask-mysql-app
```

Open in browser:

```
http://localhost:5000
```

---

## Why Gunicorn Instead of Flask Dev Server

The Flask built-in server is single-threaded and not meant for production. Gunicorn is a production-grade WSGI server that handles multiple concurrent requests using worker processes.

```bash
# What CMD runs inside the container
gunicorn -b 0.0.0.0:5000 app:app
#         |               |   |
#         bind address    |   Flask app object (app variable in app.py)
#                         Python module (app.py)
```

---

## Useful Commands

```bash
# View logs
docker logs <container-id>

# Open shell inside running container
docker exec -it <container-id> bash

# Stop and remove
docker stop <container-id>
docker rm <container-id>
```