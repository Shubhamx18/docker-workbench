<h1 align="center">🌍 Day 7 – Docker Hub, Tagging & Sharing Images</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Topic-Docker_Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Concept-Image_Sharing-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge"/>
</p>

---

## 🌐 What is Docker Hub?

**Docker Hub** is a cloud-based registry where Docker images are stored and shared.

It allows you to:
- Upload your own images  
- Download public images  
- Share images with teams  

Think of it as **GitHub for Docker Images**.

---

## 🏷 What is Image Tagging?

Tags help identify different versions of an image.

Format:

```
username/image-name:tag
```

Example:

```
shubham/myapp:v1
shubham/myapp:latest
```

---

## 🧱 Step 1 – Tag an Image Before Pushing

```bash
docker tag my-app shubham/my-app:v1
```

Now your local image is ready to be pushed to Docker Hub.

---

## 🔐 Step 2 – Login to Docker Hub

```bash
docker login
```

Enter your Docker Hub username and password.

---

## 📤 Step 3 – Push Image to Docker Hub

```bash
docker push shubham/my-app:v1
```

Your image is now stored online in Docker Hub.

---

## 📥 Step 4 – Pull Image from Docker Hub

On another system:

```bash
docker pull shubham/my-app:v1
```

This downloads the image so it can be used to run containers.

---

## 🚀 Step 5 – Run the Pulled Image

```bash
docker run -d -p 8080:80 shubham/my-app:v1
```

Now your container runs using the shared image.

---

## 🔄 Real DevOps Workflow

```
Build Image → Tag Image → Push to Docker Hub → Pull on Server → Run Container
```

This is how teams deploy applications in real environments.

---

## 📦 Using Your Own Image Remotely

Once pushed to Docker Hub, your image can be used:

✔ On cloud servers  
✔ By teammates  
✔ In CI/CD pipelines  
✔ In Kubernetes deployments  

No need to send code manually.

---

## 🧠 Best Practices for Tagging

| Practice | Reason |
|----------|--------|
| Use version tags (`v1`, `v2`) | Track changes |
| Avoid only `latest` | Not reliable in production |
| Keep naming consistent | Easier automation |

---

## 🎯 Why Image Sharing Matters in DevOps

Image sharing allows:

✔ Collaboration across teams  
✔ Consistent deployments  
✔ Easy rollback to previous versions  
✔ Faster CI/CD pipelines  

---

## 🏁 Summary

Today we learned how to tag Docker images, push them to Docker Hub, pull them on other systems, and use them remotely.

This is how containerized applications are shared and deployed in real-world DevOps environments.

---

<p align="center">
  ✅ Day 7 Complete – You can now share Docker images like a DevOps engineer
</p>
