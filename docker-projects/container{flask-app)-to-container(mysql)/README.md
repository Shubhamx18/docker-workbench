# Flask + MySQL Two-Container Docker Setup

## Overview

This project runs two Docker containers that communicate over the default Docker bridge network:

- **Container 1** — MySQL database (`mysql:latest`)
- **Container 2** — Flask web application (`flask-app`)

The Flask app connects to MySQL using the MySQL container's bridge network IP address, which is resolved at runtime via `docker inspect`.

---

## Project Structure

```
project/
├── app.py
├── Dockerfile
└── requirements.txt
```

### `requirements.txt`

```
flask
pymysql
cryptography
```

### `Dockerfile`

```dockerfile
FROM python:3.13-slim

WORKDIR /myapp

COPY app.py /myapp/
COPY requirements.txt /myapp/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

---

## Step 1 — Run the MySQL Container

Pull and start the official MySQL image with the required environment variables:

```bash
docker run -d \
  --env MYSQL_ROOT_PASSWORD="Shubham@6024" \
  --env MYSQL_DATABASE="testdb" \
  --name my-db \
  mysql:latest
```

| Flag | Value | Purpose |
|---|---|---|
| `-d` | — | Run in detached mode |
| `--env MYSQL_ROOT_PASSWORD` | `Shubham@6024` | Sets the root password |
| `--env MYSQL_DATABASE` | `testdb` | Auto-creates this database on startup |
| `--name` | `my-db` | Container name for reference |

---

## Step 2 — Get the MySQL Container IP Address

The Flask app connects to MySQL using the container's internal bridge IP. Retrieve it with:

```bash
docker inspect my-db
```

Look for the `IPAddress` field inside `NetworkSettings.Networks`:

```json
"Networks": {
    "bridge": {
        "IPAddress": "172.17.0.2"
    }
}
```

Or extract it directly:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-db
```

This IP (`172.17.0.2`) is what the Flask app uses as `DB_HOST`.

---

## Step 3 — Configure the Flask App

In `app.py`, the database connection is configured at the top:

```python
DB_HOST = '172.17.0.2'   # MySQL container IP from docker inspect
DB_USER = "root"
DB_PASSWORD = 'Shubham@6024'
DB_NAME = 'testdb'
```

The `init_db()` function retries the connection in a loop until MySQL is ready, then creates the `users` table if it does not exist and runs a migration to add the `created_at` column if it is missing.

---

## Step 4 — Build the Flask Image

From the project directory:

```bash
docker build -t flask-app .
```

---

## Step 5 — Run the Flask Container

```bash
docker run -d \
  --name flask-container \
  -p 5000:5000 \
  flask-app
```

| Flag | Value | Purpose |
|---|---|---|
| `-d` | — | Run in detached mode |
| `--name` | `flask-container` | Container name |
| `-p 5000:5000` | — | Map host port 5000 to container port 5000 |

The application will be available at:

```
http://localhost:5000
```

---

## Container Communication

Both containers run on the default Docker bridge network (`172.17.0.0/16`). The Flask container reaches MySQL directly over this network using the IP obtained from `docker inspect`.

```
Host Machine
└── Docker Bridge Network (172.17.0.0/16)
    ├── my-db            → 172.17.0.2  (MySQL, port 3306)
    └── flask-container  → 172.17.0.3  (Flask, port 5000)
```

> If the MySQL container is restarted, its IP may change. Re-run `docker inspect my-db` and update `DB_HOST` in `app.py`, then rebuild the Flask image.

---

## Application Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Renders the User Registry UI |
| `POST` | `/api/users` | Adds a new user (JSON body: `{"name": "..."}`) |
| `DELETE` | `/api/users/<id>` | Deletes a user by ID |

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The `created_at` column is added automatically via migration if it does not exist.

---

## Verify Running Containers

```bash
docker ps
```

Expected output:

```
CONTAINER ID   IMAGE        COMMAND                  PORTS                    NAMES
xxxxxxxxxxxx   flask-app    "python app.py"          0.0.0.0:5000->5000/tcp   flask-container
xxxxxxxxxxxx   mysql:latest "docker-entrypoint.s…"   3306/tcp, 33060/tcp      my-db
```

---

## Useful Commands

```bash
# View Flask app logs
docker logs flask-container

# View MySQL logs
docker logs my-db

# Open a MySQL shell inside the container
docker exec -it my-db mysql -u root -p testdb

# Stop and remove both containers
docker stop flask-container my-db
docker rm flask-container my-db
```

---

## Full Startup Sequence

```bash
# 1. Start MySQL
docker run -d --env MYSQL_ROOT_PASSWORD="Shubham@6024" --env MYSQL_DATABASE="testdb" --name my-db mysql:latest

# 2. Get MySQL IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-db

# 3. Update DB_HOST in app.py with the IP above

# 4. Build Flask image
docker build -t flask-app .

# 5. Run Flask container
docker run -d --name flask-container -p 5000:5000 flask-app

# 6. Open in browser
# http://localhost:5000
```