<h1 align="center">⚔️ Day 3 – Docker vs Virtual Machines & Core Docker Components</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Comparison-Docker_vs_VM-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Concept-Docker_Components-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Beginner--to--Intermediate-orange?style=for-the-badge"/>
</p>

---

## ⚔️ Docker vs Virtual Machines (VMs)

Before Docker, applications were deployed using **Virtual Machines**.  
Let’s understand the difference.

---

### 🖥 Virtual Machine Architecture

Each VM contains its own full operating system.

```
Application
   ↓
Guest OS
   ↓
Hypervisor
   ↓
Host OS
   ↓
Hardware
```

This makes VMs **heavy and slow to start**.

---

### 🐳 Docker Container Architecture

Containers share the host OS kernel.

```
Application
   ↓
Container
   ↓
Docker Engine
   ↓
Host OS
   ↓
Hardware
```

This makes containers **lightweight and fast**.

---

### 📊 Comparison Table

| Feature | Docker Container | Virtual Machine |
|---------|------------------|-----------------|
| OS | Shares Host OS | Full OS per VM |
| Size | Small (MBs) | Large (GBs) |
| Boot Time | Seconds | Minutes |
| Performance | Near-native | Slower |
| Resource Usage | Low | High |
| Portability | High | Moderate |

---

### 🎯 Key Takeaway

Docker containers are more efficient, faster, and easier to manage than traditional VMs.  
That’s why modern DevOps prefers **Docker over Virtual Machines**.

---

## 🧩 Core Components of Docker

Docker works using several important building blocks.

---

### 📝 1️⃣ Dockerfile

A **Dockerfile** is a set of instructions used to create a Docker image.

Example:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

### 📦 2️⃣ Docker Image

A **Docker Image** is a read-only template created from a Dockerfile.

It contains:
- Application code  
- Dependencies  
- Environment configuration  

Images are used to create containers.

---

### 🚀 3️⃣ Docker Container

A **container** is a running instance of an image.

It is:
- Isolated  
- Lightweight  
- Portable  

Command example:

```bash
docker run my-app
```

---

### 🌐 4️⃣ Docker Registry

A **registry** stores Docker images.

Examples:
- Docker Hub  
- AWS ECR  
- Private registries  

Commands:

```bash
docker push image-name
docker pull image-name
```

---

## 🔄 How These Components Work Together

```
Dockerfile → Docker Image → Docker Registry → Docker Container
```

1️⃣ Write Dockerfile  
2️⃣ Build Image  
3️⃣ Push to Registry  
4️⃣ Pull and Run Container  

---

## 🎯 Why This Matters in DevOps

Understanding these components helps you:

✔ Build portable applications  
✔ Deploy consistently  
✔ Share environments across teams  
✔ Automate CI/CD pipelines  

---

## 🏁 Summary

Today we learned the difference between Docker containers and virtual machines and explored Docker’s core components: Dockerfile, Image, Container, and Registry.

These are the fundamental building blocks of containerized applications.

---

<p align="center">
  ✅ Day 3 Complete – You now understand Docker vs VMs and Docker’s core components
</p>
