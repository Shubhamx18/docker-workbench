# 🚀 Three-Tier App — Production-Ready

A fully containerized **three-tier web application** demonstrating real-world architecture using Docker Compose.

- **Frontend**: Nginx serving a responsive dark dashboard UI  
- **Backend**: Flask REST API with health checks and DB integration  
- **Database**: MySQL 8 with persistent storage  

---

## ⚡ Quick Start

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up --build -d
🌐 Access URLs
Service	URL	Description
Frontend	http://localhost:3000
	Dashboard UI
Backend	http://localhost:5000
	Backend root (JSON)
Health	http://localhost:5000/health
	Service health check
Stats API	http://localhost:5000/api/stats
	DB + user stats
Users API	http://localhost:5000/api/users
	All users (JSON)
🏗️ Architecture
User (Browser)
      ↓
Nginx (Frontend :3000)
      ↓
Flask API (Backend :5000)
      ↓
MySQL (Database :3306 / mapped 3307)
📁 Project Structure
three-tier-app/
├── backend/
│   ├── app.py              # Flask API with health checks
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html          # Dashboard UI
│   └── Dockerfile
│
└── docker-compose.yml      # Multi-container orchestration
✨ Features
✅ 3-Tier Architecture (Frontend + Backend + Database)
✅ Docker Compose orchestration
✅ Service-to-service communication via Docker network
✅ MySQL persistent volume (mysql_data)
✅ Automatic DB initialization & seeding
✅ Flask-CORS enabled
✅ Real-time dashboard (auto-refresh)
✅ Health monitoring system
✅ Role distribution analytics
✅ User data API
🔍 Health Check System
/health endpoint verifies:
Backend status
Database connectivity (real query check)

Example response:

{
  "status": "healthy",
  "service": "backend",
  "database": "connected"
}
🧪 Sample Data

On first run, the system seeds:

5 users
Roles: admin, developer, viewer
🗄️ Database Access
From Docker container:
docker exec -it mysqldb mysql -u root -p
USE testdb;
SELECT * FROM users;
From host machine:
mysql -h localhost -P 3307 -u root -p
➕ Insert Sample Data
INSERT INTO users (name, email, role)
VALUES ('Shubham Mali', 'shubham@gmail.com', 'admin');
🔄 API Endpoints
Get all users
GET /api/users
Get stats
GET /api/stats
Health check
GET /health