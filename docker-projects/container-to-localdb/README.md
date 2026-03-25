# Container to Local Database

## What This Demonstrates

A Docker container connecting to a **MySQL database running on the host machine** (not inside another container). The container uses the special hostname `host.docker.internal` to reach the host's localhost.

---

## Project Structure

```
container-to-localdb/
├── myapp/
│   ├── Dockerfile
│   └── mycode.py
└── flask-app/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

There are two sub-projects. Both connect to a local MySQL instance using the same approach.

---

## The Key Concept — `host.docker.internal`

A container cannot use `127.0.0.1` or `localhost` to reach your host machine. From inside the container, `localhost` refers to the container itself, not your machine.

Docker provides a special hostname for this:

```
host.docker.internal
```

This hostname always resolves to the host machine's IP from inside any container. It works on macOS and Windows automatically. On Linux, you must add it manually:

```bash
docker run --add-host=host.docker.internal:host-gateway <image>
```

---

## How It Works

```
Container
└── mycode.py / app.py
        |
        | pymysql connect to host.docker.internal:3306
        |
        v
Host Machine
└── MySQL running on port 3306 (local installation)
```

---

## myapp — Simple Python Script

### `mycode.py`

```python
import pymysql

connection = pymysql.connect(
    host="host.docker.internal",   # reaches host machine's MySQL
    user="appuser",
    password="Shubham@6024",
    database="containerlocaldb",
    port=3306
)
```

It creates a `test_table` if it does not exist, inserts a row, and prints all rows.

### `myapp/Dockerfile`

```dockerfile
FROM python:latest

WORKDIR /myapp

COPY mycode.py /myapp/

RUN pip install pymysql

CMD ["python", "mycode.py"]
```

### Build and Run

```bash
cd myapp

docker build -t local-db-app .

# macOS / Windows
docker run local-db-app

# Linux — must pass the host-gateway flag
docker run --add-host=host.docker.internal:host-gateway local-db-app
```

---

## flask-app — Full Flask Web App

The Flask app connects to the same local MySQL instance using `host.docker.internal` as the host and exposes a web UI on port 5000.

### `flask-app/Dockerfile`

```dockerfile
FROM python:3.13.12-slim

WORKDIR /myapp

COPY app.py /myapp/
COPY requirements.txt /myapp/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

### Build and Run

```bash
cd flask-app

docker build -t flask-local-db .

# macOS / Windows
docker run -p 5000:5000 flask-local-db

# Linux
docker run --add-host=host.docker.internal:host-gateway -p 5000:5000 flask-local-db
```

Open in browser:

```
http://localhost:5000
```

---

## Prerequisites on Host Machine

Before running the container, ensure MySQL is running locally and the required database and user exist:

```sql
CREATE DATABASE containerlocaldb;
CREATE USER 'appuser'@'%' IDENTIFIED BY 'Shubham@6024';
GRANT ALL PRIVILEGES ON containerlocaldb.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
```

The `%` wildcard allows connections from any host, including Docker containers.

---

## Why `host.docker.internal` and Not `127.0.0.1`

| Address | From Container | Reaches |
|---|---|---|
| `127.0.0.1` | Inside container | Container itself — not the host |
| `host.docker.internal` | Inside container | Host machine's network |

Using `127.0.0.1` inside a container will fail with a connection refused error because there is no MySQL running inside the container.