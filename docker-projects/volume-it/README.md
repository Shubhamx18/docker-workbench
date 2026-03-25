# Docker Volumes

## What is a Docker Volume

A Docker volume is a storage area managed by Docker that lives **outside the container's filesystem**. When a container writes data to a volume, that data persists even after the container is stopped or deleted.

Without a volume, any file written inside a container is lost the moment the container is removed. With a volume, the data survives.

---

## Project Structure

```
volume-it/
└── myapp/
    ├── Dockerfile
    ├── myapp.py
    └── data.txt
```

The app takes user input, appends it to `data.txt`, and optionally displays all saved entries. If `data.txt` is stored inside a volume, data persists across multiple container runs.

---

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /myapp

COPY . .

CMD ["python", "myapp.py"]
```

---

## Step 1 — Create a Named Volume

```bash
docker volume create myvolume
```

Docker creates a managed storage area on the host. You do not need to know where it lives — Docker handles the path.

---

## Step 2 — Build the Image

```bash
docker build -t volume-app .
```

---

## Step 3 — Run with the Volume

```bash
docker run -it -v myvolume:/myapp volume-app
```

| Part | Meaning |
|---|---|
| `-it` | Interactive mode — needed because the app reads user input |
| `-v myvolume:/myapp` | Mount the named volume `myvolume` at `/myapp` inside the container |
| `volume-app` | The image to run |

When the app writes to `data.txt` inside `/myapp`, that file is stored in `myvolume`. The next time you run the container with the same volume, the data is still there.

---

## Step 4 — Inspect the Volume

List all volumes on the system:

```bash
docker volume ls
```

Output:

```
DRIVER    VOLUME NAME
local     myvolume
```

Inspect a specific volume for details:

```bash
docker volume inspect myvolume
```

Output:

```json
[
    {
        "CreatedAt": "2026-03-25T10:00:00Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/myvolume/_data",
        "Name": "myvolume",
        "Options": {},
        "Scope": "local"
    }
]
```

The `Mountpoint` is where Docker stores the volume data on the host. You can inspect the files there directly if needed (requires root on Linux).

---

## Volume vs Bind Mount

| | Volume | Bind Mount |
|---|---|---|
| Managed by | Docker | You |
| Location on host | Docker chooses | You specify |
| Survives container deletion | Yes | Yes |
| Best for | Persistent app data (databases, logs, uploads) | Sharing host files with container |

---

## Useful Volume Commands

```bash
# Create a volume
docker volume create myvolume

# List all volumes
docker volume ls

# Inspect a volume
docker volume inspect myvolume

# Remove a volume (only when no container is using it)
docker volume rm myvolume

# Remove all unused volumes
docker volume prune
```

---

## Run Sequence Summary

```bash
# 1. Create volume
docker volume create myvolume

# 2. Build image
docker build -t volume-app .

# 3. Run container with volume attached
docker run -it -v myvolume:/myapp volume-app

# 4. Run again — data.txt still has the previous entries
docker run -it -v myvolume:/myapp volume-app

# 5. Check volume details
docker volume inspect myvolume
```

Each run of the container appends to the same `data.txt` because both runs share the same volume.