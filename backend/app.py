from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
import os
import time
import datetime

app = Flask(__name__)
CORS(app)

# ---------------- CONFIG ---------------- #

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysqldb"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "testdb"),
    "connect_timeout": 5
}

# ---------------- DB CONNECTION ---------------- #

def get_connection():
    return pymysql.connect(**DB_CONFIG)


def wait_for_db():
    retries = 0
    while retries < 15:
        try:
            conn = get_connection()
            conn.close()
            print("✅ Connected to MySQL")
            return
        except Exception as e:
            retries += 1
            print(f"⏳ Waiting for MySQL... ({retries}): {e}")
            time.sleep(3)

    print("❌ DB not ready after retries")


def check_db():
    """Robust DB health check"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        conn.close()
        return True
    except Exception as e:
        print("❌ DB Health Error:", e)
        return False


def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                role VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        if count == 0:
            users = [
                ("Alice Johnson", "alice@example.com", "admin"),
                ("Bob Smith", "bob@example.com", "developer"),
                ("Carol White", "carol@example.com", "developer"),
                ("Dave Brown", "dave@example.com", "viewer"),
                ("Eve Davis", "eve@example.com", "viewer"),
            ]
            cursor.executemany(
                "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)",
                users
            )
            conn.commit()
            print("🌱 Seed data inserted")

        cursor.close()
        conn.close()

    except Exception as e:
        print("⚠️ DB Init Error:", e)


# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "🚀 Three-Tier Backend",
        "version": "3.0",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


# 🔥 FINAL HEALTH CHECK (FIXED)
@app.route("/health")
def health():
    db_status = "connected" if check_db() else "disconnected"

    return jsonify({
        "status": "healthy",
        "service": "backend",
        "database": db_status,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/api/stats")
def stats():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        roles = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "total_users": total_users,
            "roles": roles,
            "db_version": db_version,
            "db_name": DB_CONFIG["database"],
            "database_status": "connected"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "database_status": "disconnected"
        }), 500


@app.route("/api/users")
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM users ORDER BY id")
        users = cursor.fetchall()

        for u in users:
            if u.get("created_at"):
                u["created_at"] = str(u["created_at"])

        cursor.close()
        conn.close()

        return jsonify({
            "users": users,
            "count": len(users)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)