<h1 align="center">🧱 Day 6 – Image Management & Interactive Containers</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Docker_Images-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Image_Management-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Mode-Interactive_Containers-orange?style=for-the-badge"/>
</p>

---

## 📦 What is a Docker Image?

A **Docker Image** is a read-only template used to create containers.

It contains:
- Application code  
- Dependencies  
- Libraries  
- System tools  
- Runtime environment  

> 🧠 Image = Blueprint  
> 🚀 Container = Running instance of the blueprint

---

## 📋 Listing Docker Images

```bash
docker images
```

Shows all images stored on your system.

---

## 🏷 Tagging an Image

Tags help manage different versions of images.

```bash
docker tag nginx my-nginx:v1
```

Now `my-nginx:v1` is another name for the same image.

---

## 🗑 Removing an Image

```bash
docker rmi image_id
```

Deletes an image from your system.

---

## 🛠 Making Changes to a Running Container

Sometimes you may want to test changes manually.

Step 1: Run container in interactive mode

```bash
docker run -it ubuntu /bin/bash
```

Now you are inside the container.

Step 2: Install something

```bash
apt update
apt install curl
```

Step 3: Exit container

```bash
exit
```

---

## 💾 Saving Changes as a New Image

After modifying a container, save it as a new image:

```bash
docker commit container_id my-ubuntu:v2
```

This creates a new image with your changes.

---

## 🧱 Using Predefined/Base Images

Docker Hub provides many base images:

- `ubuntu`
- `alpine`
- `node`
- `python`
- `mysql`

Pull an image:

```bash
docker pull python:3.10
```

These images save time because they already contain common tools.

---

## 🧪 Interactive Mode Explained

Interactive mode lets you interact with the container using a terminal.

```bash
docker run -it ubuntu
```

| Flag | Meaning |
|------|---------|
| `-i` | Interactive mode (keep STDIN open) |
| `-t` | Allocate terminal |

Useful for:
✔ Testing  
✔ Debugging  
✔ Learning Linux inside containers  

---

---

## 🧠 When Do We Use Interactive Mode?

Interactive mode is mainly used for:

| Use Case | Why We Use It |
|----------|---------------|
| 🧪 Testing software | Try commands inside container |
| 🐞 Debugging issues | Check logs, files, configs manually |
| 📦 Exploring base images | See what tools are installed |
| 🎓 Learning Linux | Practice commands in safe environment |

Example:

```bash
docker run -it ubuntu /bin/bash
```

This opens a terminal inside the container.

⚠️ In real production DevOps, interactive mode is **rarely used** because containers are meant to run automatically.

---

## ⚙️ How Interactive Behavior Relates to Docker Compose (YAML)

In Docker Compose, we don’t usually use `-it` like CLI, but we can configure similar behavior using YAML options.

### Example `docker-compose.yml`

```yaml
version: "3.9"

services:
  ubuntu-test:
    image: ubuntu
    container_name: ubuntu_interactive
    stdin_open: true   # Equivalent to -i
    tty: true          # Equivalent to -t
```

| YAML Option | Equivalent CLI Flag | Purpose |
|-------------|---------------------|---------|
| `stdin_open: true` | `-i` | Keeps STDIN open |
| `tty: true` | `-t` | Allocates terminal |

Run it:

```bash
docker compose up
```

Then enter container:

```bash
docker exec -it ubuntu_interactive bash
```

---

## 🎯 Key DevOps Note

Interactive mode is mainly for:

✔ Development  
✔ Debugging  
✔ Learning  

In **production**, containers usually run in **detached mode** with automated logs and monitoring.


## 🔄 Image Lifecycle

```
Pull → Build → Run → Modify → Commit → Tag → Push → Remove
```

Images can be updated and versioned just like code.

---

## 🎯 Why Image Management Matters in DevOps

DevOps engineers need to:

✔ Maintain multiple image versions  
✔ Optimize image size  
✔ Rebuild images when app changes  
✔ Use trusted base images  

Image management ensures consistent deployments.

---

## 🏁 Summary

Today we learned how to manage Docker images, make changes inside containers, save those changes as new images, and use interactive mode for testing and debugging.

---

<p align="center">
  ✅ Day 6 Complete – You now understand Docker Image Management and Interactive Containers
</p>
