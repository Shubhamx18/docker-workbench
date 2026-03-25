# Docker Hub & Image Registry

## What is Docker Hub?

Docker Hub is the default cloud-based registry where Docker images are stored, versioned, and distributed.

It allows you to:
- Upload and publish your own images
- Download thousands of official public images
- Share images across teams and environments

> Think of it as GitHub but for Docker Images.

---

## Types of Registries

| Registry | Type | Best For |
|----------|------|----------|
| Docker Hub | Public / Private | Personal projects, open source |
| AWS ECR | Private | AWS-based production deployments |
| GitHub Container Registry | Private | GitHub Actions CI/CD pipelines |
| Google Container Registry | Private | GCP-based deployments |
| Self-hosted (Harbor) | Private | On-premise enterprise environments |

---

## Image Tagging Convention

Tags identify different versions or variants of an image.

```
username/image-name:tag
```

Examples:

```bash
shubham/my-app:v1
shubham/my-app:v2.0.1
shubham/my-app:latest
shubham/my-app:prod
shubham/my-app:dev
```

---

## Complete Push / Pull Workflow

### Step 1 — Build the Image

```bash
docker build -t my-app .
```

### Step 2 — Tag for Docker Hub

```bash
docker tag my-app shubham/my-app:v1
```

### Step 3 — Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

### Step 4 — Push to Docker Hub

```bash
docker push shubham/my-app:v1
```

Your image is now publicly accessible on Docker Hub.

### Step 5 — Pull on Another Machine

```bash
docker pull shubham/my-app:v1
```

### Step 6 — Run the Image

```bash
docker run -d -p 8080:80 shubham/my-app:v1
```

---

## Where Your Image Can Be Used After Pushing

Once pushed to Docker Hub, the image is ready for:

- Cloud servers (AWS EC2, GCP, Azure VM)
- Other team members (no need to send code manually)
- CI/CD pipelines (GitHub Actions, Jenkins, GitLab CI)
- Kubernetes deployments

---

## Tagging Best Practices

| Practice | Why It Matters |
|----------|----------------|
| Always use version tags (`v1`, `v2`) | Clearly track changes over time |
| Never rely only on `latest` | `latest` is ambiguous and risky in production |
| Use semantic versioning (`1.0.0`) | Industry standard for version tracking |
| Tag for environment (`prod`, `dev`) | Separate pipelines cleanly |
| Keep naming consistent | Enables easier automation in CI/CD |

---

## Full DevOps Workflow with Registry

```
Write Code
    │
    ▼
Build Image  ──────────────  docker build -t my-app .
    │
    ▼
Tag Image  ────────────────  docker tag my-app shubham/my-app:v1
    │
    ▼
Push to Registry  ─────────  docker push shubham/my-app:v1
    │
    ▼
Pull on Server  ───────────  docker pull shubham/my-app:v1
    │
    ▼
Run Container  ────────────  docker run -d -p 80:80 shubham/my-app:v1
```

---

## Logging Out

```bash
docker logout
```

Always logout on shared machines to protect your credentials.

---

## Why Image Sharing Matters in DevOps

- Enables consistent collaboration across distributed teams
- Ensures every environment uses the exact same image
- Supports easy rollback by pulling any previous image version
- Accelerates CI/CD pipelines with pre-built images
