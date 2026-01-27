<h1 align="center">🚀 Day 5 – Running Containers & Container Management</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Running_Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Container_Management-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge"/>
</p>

---

## 🐳 Running a Docker Container

To run a container from an image:

```bash
docker run nginx
```

This command:
- Pulls the image (if not available locally)
- Creates a container
- Starts the application

---

## 🔌 Running a Container in Detached Mode

By default, containers run in the foreground.  
To run in the background (detached mode):

```bash
docker run -d nginx
```

`-d` = detached mode  
Container runs in the background.

---

## 🌍 Running Container with Port Mapping

To access a container’s application from your browser:

```bash
docker run -d -p 8080:80 nginx
```

This means:
- Host port **8080** → Container port **80**

Open in browser:  
`http://localhost:8080`

---

## 🧪 Running Multiple Containers

You can run multiple containers from the same image:

```bash
docker run -d -p 8081:80 nginx
docker run -d -p 8082:80 nginx
```

Each container runs independently.

---

## 📋 Listing Containers

### Show running containers

```bash
docker ps
```

### Show all containers (running + stopped)

```bash
docker ps -a
```

---

## ⏹ Stopping a Container

```bash
docker stop container_id
```

Stops a running container.

---

## ▶️ Starting a Stopped Container

```bash
docker start container_id
```

---

## 🔁 Restarting a Container

```bash
docker restart container_id
```

---

## ❌ Removing a Container

First stop it:

```bash
docker stop container_id
```

Then remove it:

```bash
docker rm container_id
```

---

## 📜 Viewing Container Logs

To see application output:

```bash
docker logs container_id
```

---

## 💻 Executing Commands Inside a Running Container

```bash
docker exec -it container_id /bin/bash
```

This opens a terminal inside the container.

`-it` = interactive terminal

---

## 🧠 Container Lifecycle

```
Create → Start → Run → Stop → Remove
```

Docker allows full control of this lifecycle.

---

## 🎯 Why Container Management Matters in DevOps

DevOps engineers need to:

✔ Monitor running applications  
✔ Restart failed containers  
✔ View logs for debugging  
✔ Manage multiple services  

Understanding container commands is essential for real-world deployments.

---

## 🏁 Summary

Today we learned how to run containers, use detached mode, map ports, manage multiple containers, and control the container lifecycle using Docker commands.

---

<p align="center">
  ✅ Day 5 Complete – You can now run and manage Docker containers
</p>
