<h1 align="center">📝 Dockerfile Fundamentals</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Dockerfile-blue?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Image_Building-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge"/>
</p>

---

## 📝 What is a Dockerfile?

A **Dockerfile** is a plain text file containing sequential instructions that Docker executes to automatically build an image.

It defines:
- The base operating system or runtime
- Files and code to copy into the image
- Dependencies to install
- Commands to run the application

> Think of it as a **recipe** — follow the steps and you always get the same result 🍳

---

## 📦 Why Dockerfiles Matter

| Without Dockerfile | With Dockerfile |
|--------------------|-----------------|
| ❌ Manual environment setup every time | ✔ Fully automated image creation |
| ❌ Inconsistent environments across machines | ✔ Identical environment every single time |
| ❌ No way to version your environment | ✔ Version control your entire app setup |
| ❌ Onboarding new devs is slow | ✔ One command to reproduce the full environment |

---

## 🧱 Complete Dockerfile Example

```dockerfile
# ── Base Image ────────────────────────────────
FROM python:3.10-slim

# ── Metadata ──────────────────────────────────
LABEL maintainer="shubham@example.com"
LABEL version="1.0"

# ── Environment Variables ─────────────────────
ENV APP_ENV=production
ENV PORT=5000

# ── Working Directory ─────────────────────────
WORKDIR /app

# ── Copy & Install Dependencies ───────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy Application Code ─────────────────────
COPY . .

# ── Declare Port ─────────────────────────────
EXPOSE 5000

# ── Startup Command ───────────────────────────
CMD ["python", "app.py"]
```

---

## 🔍 Dockerfile Instruction Reference

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Set the base image | `FROM node:18-alpine` |
| `WORKDIR` | Set working directory inside container | `WORKDIR /app` |
| `COPY` | Copy files from host into image | `COPY . .` |
| `ADD` | Like COPY but also supports URLs and tar extraction | `ADD app.tar.gz /app` |
| `RUN` | Execute commands during build (creates a new layer) | `RUN npm install` |
| `CMD` | Default command when container starts (overridable) | `CMD ["node", "server.js"]` |
| `ENTRYPOINT` | Fixed executable that always runs | `ENTRYPOINT ["python"]` |
| `EXPOSE` | Document which port the app listens on | `EXPOSE 3000` |
| `ENV` | Set environment variables | `ENV NODE_ENV=production` |
| `ARG` | Build-time variable (not available at runtime) | `ARG VERSION=1.0` |
| `VOLUME` | Declare a mount point for persistent storage | `VOLUME /data` |
| `LABEL` | Add metadata to the image | `LABEL version="1.0"` |
| `USER` | Set the user for subsequent commands | `USER node` |

---

## 🧠 CMD vs ENTRYPOINT

| | CMD | ENTRYPOINT |
|-|-----|------------|
| Purpose | Default command | Fixed executable |
| Can be overridden? | ✅ Yes, at runtime | ❌ No (only arguments change) |
| Best for | Flexible default commands | Wrapping a specific tool |

```dockerfile
# CMD — can be fully overridden
CMD ["python", "app.py"]

# ENTRYPOINT — python always runs, only arguments change
ENTRYPOINT ["python"]
CMD ["app.py"]       # default arg — run as: python app.py
```

---

## 🏗 Build Commands

```bash
# Build image from Dockerfile in current directory
docker build -t my-app:v1 .

# Build using a specific Dockerfile name
docker build -f Dockerfile.prod -t my-app:prod .

# Build with a build argument
docker build --build-arg VERSION=2.0 -t my-app:v2 .

# Show build layers and history
docker history my-app:v1
```

---

## 🚀 Multi-Stage Builds (Best Practice)

Multi-stage builds produce smaller, leaner production images by separating the build environment from the runtime environment.

```dockerfile
# ── Stage 1: Build ────────────────────────────
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ── Stage 2: Production ───────────────────────
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

> ✅ The final image contains only the output — not the full build tools — keeping it small and secure.

---

## 🔒 Dockerfile Security Best Practices

```dockerfile
# ✅ Use specific version tags — never just "latest"
FROM python:3.10-slim        # Good
FROM python:latest           # ❌ Unpredictable

# ✅ Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# ✅ Install only what you need
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy dependency files before source code (layer caching)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .                     # Source changes don't bust the cache above
```

---

## 🎯 Why Dockerfiles Matter in DevOps

✔ Fully automated, repeatable image builds
✔ Environment-as-code — stored in version control alongside the app
✔ Foundation for every CI/CD pipeline
✔ Enables rollback by rebuilding any previous version

---

<p align="center">
  ✅ Topic Complete — You now understand how to write, build, and optimize Dockerfiles
</p>
