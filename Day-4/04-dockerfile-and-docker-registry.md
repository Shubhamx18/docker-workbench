<h1 align="center">📝 Day 4 – Dockerfile & Docker Registry</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Dockerfile-blue?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Docker_Registry-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge"/>
</p>

---

## 📝 What is a Dockerfile?

A **Dockerfile** is a text file that contains instructions to automatically build a Docker image.

It defines:
- Base operating system  
- Application code  
- Dependencies  
- Commands to run the application  

Think of it as a **recipe** for creating a Docker image 🍳

---

## 📦 Why Dockerfile is Important

Without Dockerfile:
❌ Manual setup every time  
❌ Hard to reproduce environments  

With Dockerfile:
✔ Automated image creation  
✔ Same environment every time  
✔ Easy version control  

---

## 🧱 Basic Structure of a Dockerfile

Here is a simple example:

```dockerfile
# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files from local system to container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Command to run when container starts
CMD ["python", "app.py"]
```

---

## 🔍 Explanation of Common Dockerfile Instructions

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Specifies base image |
| `WORKDIR` | Sets working directory inside container |
| `COPY` | Copies files into container |
| `RUN` | Executes commands during build |
| `CMD` | Default command when container starts |
| `EXPOSE` | Tells which port the app uses |
| `ENV` | Sets environment variables |

---

## 🏗 How Dockerfile Creates an Image

```bash
docker build -t my-app:v1 .
```

This command:
1️⃣ Reads the Dockerfile  
2️⃣ Executes each instruction  
3️⃣ Creates a Docker Image  

---

## 🌐 What is a Docker Registry?

A **Docker Registry** is a storage system for Docker images.

It allows teams to share images across environments.

Examples:
- Docker Hub (public)  
- AWS ECR  
- Google Container Registry  
- Private company registry  

---

## 🔄 Working with Docker Registry

### 📤 Push Image to Registry

```bash
docker push username/my-app:v1
```

Uploads your image to Docker Hub.

---

### 📥 Pull Image from Registry

```bash
docker pull username/my-app:v1
```

Downloads image to your system.

---

## 🧠 Real-World Workflow

```
Dockerfile → Build Image → Push to Registry → Pull on Server → Run Container
```

This is how applications move from development to production.

---

## 🎯 Why Dockerfile & Registry Matter in DevOps

They help in:

✔ Automating application builds  
✔ Sharing images across teams  
✔ Version controlling environments  
✔ Enabling CI/CD pipelines  

---

## 🏁 Summary

A Dockerfile is used to create Docker images automatically.  
A Docker Registry is used to store and share those images.

Together, they make application deployment fast, consistent, and reliable in DevOps environments.

---

<p align="center">
  ✅ Day 4 Complete – You now understand Dockerfile and Docker Registry
</p>
