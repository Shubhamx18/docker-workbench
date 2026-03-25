# Bind Mounts

## What is a Bind Mount

A bind mount links a directory or file on the **host machine** directly into a directory inside the **container**. Whatever exists on the host path is what the container sees — in real time. There is no copy involved.

Use it when you want to give a container access to files that already exist on your machine without baking them into the image.

---

## Project Structure

```
bind-mounts/
├── Dockerfile
├── myapp.py
└── servers.txt
```

The Python script `myapp.py` reads `servers.txt` line by line and prints each server entry. The file is **not** copied into the image. It is mounted in at runtime.

---

## How It Works

```
Host Machine
└── /absolute/path/to/bind-mounts/servers.txt
        |
        | (bind mount -v)
        |
Container
└── /myapp/servers.txt   <-- same file, not a copy
```

Any edit you make to `servers.txt` on the host is immediately visible inside the container. No rebuild needed.

---

## Step 1 — Build the Image

```bash
docker build -t bind-app .
```

The `Dockerfile` copies only `myapp.py` into the image. `servers.txt` is intentionally left out.

```dockerfile
FROM python:3.13.12-slim

WORKDIR /myapp

COPY myapp.py /myapp/

CMD ["python", "myapp.py"]
```

---

## Step 2 — Run with Bind Mount

```bash
docker run -v /absolute/host/path/servers.txt:/myapp/servers.txt bind-app
```

| Part | Meaning |
|---|---|
| `-v` | Flag to declare a volume or bind mount |
| `/absolute/host/path/servers.txt` | Full path to the file on your host machine |
| `/myapp/servers.txt` | Path inside the container where it appears |

Example on macOS / Linux:

```bash
docker run -v $(pwd)/servers.txt:/myapp/servers.txt bind-app
```

---

## Why Use Bind Mounts

Without a bind mount, you would have to `COPY` the file into the image and rebuild every time it changes. With a bind mount:

- The container reads the live file from your host
- You edit the file on your host and the container sees it instantly
- No rebuild, no re-copy

This is especially useful for config files, log directories, or any file that changes frequently during development.

---

## servers.txt Format

```
# Production Servers
192.168.1.10
192.168.1.11

# Staging Servers
192.168.2.20
192.168.2.21

# Development Servers
dev-server-01.local
dev-server-02.local

# Cloud Instances
ec2-13-233-101-45.compute-1.amazonaws.com
ec2-65-0-122-88.compute-1.amazonaws.com
```

The script skips empty lines and comment lines automatically.

---

## Expected Output

```
Reading servers from servers.txt...

1. 192.168.1.10
2. 192.168.1.11
3. 192.168.2.20
4. 192.168.2.21
5. dev-server-01.local
6. dev-server-02.local
7. ec2-13-233-101-45.compute-1.amazonaws.com
8. ec2-65-0-122-88.compute-1.amazonaws.com

File processed successfully.
Program execution completed.
```