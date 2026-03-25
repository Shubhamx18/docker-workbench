# Three-Tier Application

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
        | serves index.html
        |
        v
Flask Container (backend) :5000
        |
        | pymysql connection
        |
        v
MySQL Container (mysqldb) :3306
        |
        v
Returns rows → Flask formats JSON → browser renders dashboard
```

All three containers share `app-network` defined in Docker Compose.
MySQL is never exposed to the browser directly. Flask is the only service
that talks to the database.

---

## Backend

**backend/Dockerfile** — builds a slim Python image, installs dependencies, and runs `app.py` on port 5000.

**backend/requirements.txt** — declares four dependencies: `flask`, `flask-cors`, `pymysql`, and `cryptography`.

**backend/app.py** — the Flask application does four things:

- Waits for MySQL to be ready on startup, retrying every 3 seconds up to 15 times
- Creates the `users` table if it does not exist and seeds five sample records
- Exposes `/health` to report backend and database status
- Exposes `/api/users` and `/api/stats` to return user records and aggregate counts

The database host, name, user, and password are all read from environment variables
so the same image works in any environment without rebuilding.

---

## Frontend

**frontend/Dockerfile** — builds from `nginx:alpine`, drops in `index.html`, and writes
a minimal Nginx config that serves the file on port 80 and falls back to `index.html`
for any unknown path.

**frontend/index.html** — a single-page dashboard that fetches from the Flask API on load,
renders a user table, shows service health status, and logs activity in real time.
No build step. No bundler. Pure HTML, CSS, and vanilla JavaScript.

---

## Docker Compose

**docker-compose.yml** wires everything together:

- `mysqldb` — runs MySQL 8 with a named volume for persistent storage, exposed on host port 3307
- `backend` — builds from `./backend`, receives DB credentials as environment variables, depends on `mysqldb`
- `frontend` — builds from `./frontend`, exposed on host port 3000, depends on `backend`
- All three services share `app-network` so they resolve each other by service name

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

## Endpoints

```
GET  http://localhost:3000           → dashboard UI
GET  http://localhost:5000/health    → backend and database status
GET  http://localhost:5000/api/users → all users from MySQL
GET  http://localhost:5000/api/stats → totals, role breakdown, DB version
```

---

## Database Access

```bash
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

Docker Compose handles all networking automatically. Containers resolve each other
by service name — Flask connects to MySQL simply by using `mysqldb` as the host.

You do not need to hardcode IP addresses, expose MySQL to the host, or configure
any manual DNS. The only port the browser ever touches is `3000`.
Everything behind it stays internal.
