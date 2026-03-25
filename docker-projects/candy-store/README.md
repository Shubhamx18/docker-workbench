# Candy Store — Node.js Static Web App in Docker

## What This Demonstrates

A minimal Node.js + Express web server containerized with Docker. It serves a static HTML page with an image and CSS from the `public/` folder. This is the simplest form of a Dockerized web application — no database, no API, just a server that delivers static files.

---

## Project Structure

```
candy-store/
├── Dockerfile
├── app.js
├── package.json
└── public/
    ├── index.html
    ├── style.css
    └── canddy.webp
```

---

## How It Works

```
Browser
    |
    | HTTP GET http://localhost:3000
    |
    v
Container (port 3000)
└── Express server (app.js)
        |
        | express.static('public')
        v
    Serves index.html, style.css, canddy.webp
```

Express is configured to serve everything inside the `public/` directory as static files. Any file placed in `public/` is accessible directly via the browser.

---

## app.js

```js
const express = require('express');
const app = express();
const port = 3000;

app.use(express.static('public'));

app.listen(port, () => {
    console.log(`Candy store app listening at http://localhost:${port}`);
});
```

---

## Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app/

COPY . .

RUN npm install

CMD ["node", "app.js"]
```

| Instruction | Purpose |
|---|---|
| `FROM node:18-alpine` | Lightweight Node.js 18 base image |
| `WORKDIR /app/` | All commands run from this directory |
| `COPY . .` | Copies all project files including `public/` |
| `RUN npm install` | Installs Express from `package.json` |
| `CMD ["node", "app.js"]` | Starts the server when the container runs |

---

## Step 1 — Build the Image

```bash
docker build -t candy-store .
```

---

## Step 2 — Run the Container

```bash
docker run -d -p 3000:3000 candy-store
```

| Flag | Meaning |
|---|---|
| `-d` | Run in detached (background) mode |
| `-p 3000:3000` | Map host port 3000 to container port 3000 |

---

## Step 3 — Open in Browser

```
http://localhost:3000
```

The page displays the IceCream Brand landing page with a pink header, a product image, and styled layout.

---

## Useful Commands

```bash
# View running container
docker ps

# View logs
docker logs <container-id>

# Stop the container
docker stop <container-id>

# Remove the container
docker rm <container-id>
```