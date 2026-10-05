import os
import csv
import io
import time
from flask import Flask, render_template_string, request, jsonify, Response
from dbutils.pooled_db import PooledDB
import pymysql

app = Flask(__name__)

db_config = {
    'host': "host.docker.internal",    # for local = localhost, for docker = host.docker.internal
    'user': "appuser",
    'password': "Shubham@6024",
    'database': "hello",
    'cursorclass': pymysql.cursors.DictCursor
}

pool = PooledDB(creator=pymysql, mincached=2, maxcached=10, **db_config)


def init_db():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                sort_order INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """)
            # Add sort_order column if upgrading from old schema
            try:
                cur.execute("ALTER TABLE test_table ADD COLUMN sort_order INT DEFAULT 0")
            except:
                pass
            try:
                cur.execute("ALTER TABLE test_table ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            except:
                pass
            conn.commit()


def validate_name(name):
    if not name or not name.strip():
        return None, "Name cannot be empty"
    name = name.strip()
    if len(name) > 100:
        return None, "Name too long (max 100 characters)"
    return name, None


@app.route("/")
def index():
    sort = request.args.get("sort", "id_desc")
    order_map = {
        "id_desc": "id DESC",
        "id_asc": "id ASC",
        "name_asc": "name ASC",
        "name_desc": "name DESC",
        "custom": "sort_order ASC, id DESC"
    }
    order = order_map.get(sort, "id DESC")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM test_table ORDER BY {order}")
            rows = cur.fetchall()
    return render_template_string(HTML, rows=rows, sort=sort)


@app.route("/add", methods=["POST"])
def add():
    name, err = validate_name(request.json.get("name", ""))
    if err:
        return jsonify({"ok": False, "error": err}), 400
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as cnt FROM test_table WHERE name = %s", (name,))
            if cur.fetchone()["cnt"] > 0:
                return jsonify({"ok": False, "error": "Name already exists"}), 409
            cur.execute("INSERT INTO test_table (name, sort_order) VALUES (%s, (SELECT COALESCE(MAX(sort_order),0)+1 FROM test_table t2))", (name,))
            conn.commit()
            new_id = cur.lastrowid
            cur.execute("SELECT * FROM test_table WHERE id=%s", (new_id,))
            row = cur.fetchone()
    return jsonify({"ok": True, "row": {
        "id": row["id"],
        "name": row["name"],
        "created_at": row["created_at"].strftime("%b %d, %Y")
    }})


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM test_table WHERE id=%s", (id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"ok": False, "error": "Not found"}), 404
            cur.execute("DELETE FROM test_table WHERE id=%s", (id,))
            conn.commit()
    return jsonify({"ok": True, "deleted_name": row["name"]})


@app.route("/delete-bulk", methods=["POST"])
def delete_bulk():
    ids = request.json.get("ids", [])
    if not ids:
        return jsonify({"ok": False, "error": "No IDs provided"}), 400
    placeholders = ",".join(["%s"] * len(ids))
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM test_table WHERE id IN ({placeholders})", ids)
            conn.commit()
            deleted = cur.rowcount
    return jsonify({"ok": True, "deleted": deleted})


@app.route("/edit/<int:id>", methods=["PUT"])
def edit(id):
    name, err = validate_name(request.json.get("name", ""))
    if err:
        return jsonify({"ok": False, "error": err}), 400
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM test_table WHERE id=%s", (id,))
            if not cur.fetchone():
                return jsonify({"ok": False, "error": "Not found"}), 404
            cur.execute("UPDATE test_table SET name=%s WHERE id=%s", (name, id))
            conn.commit()
    return jsonify({"ok": True, "name": name})


@app.route("/reorder", methods=["POST"])
def reorder():
    order = request.json.get("order", [])
    with pool.connection() as conn:
        with conn.cursor() as cur:
            for i, item_id in enumerate(order):
                cur.execute("UPDATE test_table SET sort_order=%s WHERE id=%s", (i, item_id))
            conn.commit()
    return jsonify({"ok": True})


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM test_table WHERE name LIKE %s ORDER BY name ASC LIMIT 10", (f"%{q}%",))
            rows = cur.fetchall()
    return jsonify(rows)


@app.route("/stats")
def stats():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM test_table")
            total = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) as today FROM test_table WHERE DATE(created_at) = CURDATE()")
            today = cur.fetchone()["today"]
            cur.execute("SELECT COUNT(*) as week FROM test_table WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)")
            week = cur.fetchone()["week"]
            cur.execute("SELECT name FROM test_table ORDER BY id DESC LIMIT 1")
            last = cur.fetchone()
    return jsonify({
        "total": total,
        "today": today,
        "week": week,
        "latest": last["name"] if last else "—"
    })


@app.route("/export")
def export():
    fmt = request.args.get("fmt", "csv")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM test_table ORDER BY id ASC")
            rows = cur.fetchall()

    if fmt == "json":
        data = [{"id": r["id"], "name": r["name"], "created_at": str(r["created_at"])} for r in rows]
        return Response(
            __import__("json").dumps(data, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment; filename=users.json"}
        )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Created At"])
    for r in rows:
        writer.writerow([r["id"], r["name"], r["created_at"]])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NEXUS — User Registry</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">

<style>
:root {
  --bg:        #03050a;
  --surface:   #080d18;
  --surface2:  #0d1526;
  --border:    rgba(0,200,255,0.10);
  --border2:   rgba(0,200,255,0.22);
  --cyan:      #00c8ff;
  --violet:    #9b5cff;
  --green:     #00ffb2;
  --red:       #ff4060;
  --amber:     #ffb800;
  --text:      #e8f4ff;
  --muted:     rgba(232,244,255,0.45);
  --card-bg:   rgba(13,21,38,0.85);
  --glow-c:    rgba(0,200,255,0.15);
  --glow-v:    rgba(155,92,255,0.15);
  --r:         14px;
  --font:      'Syne', sans-serif;
  --mono:      'DM Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── ANIMATED BACKGROUND ─────────────────────────────────── */
#bg-canvas {
  position: fixed; inset: 0; z-index: 0;
  pointer-events: none;
}

/* ── LAYOUT ───────────────────────────────────────────────── */
.shell {
  position: relative; z-index: 1;
  max-width: 780px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

/* ── HEADER ───────────────────────────────────────────────── */
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 38px;
}

.logo {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-tag {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--cyan);
  letter-spacing: 4px;
  text-transform: uppercase;
  opacity: 0.7;
}

.logo-name {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  background: linear-gradient(100deg, var(--cyan) 0%, var(--violet) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* ── STATS BAR ────────────────────────────────────────────── */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}

.stat-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 16px 18px;
  position: relative;
  overflow: hidden;
  transition: border-color .3s, transform .3s;
}

.stat-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--glow-c);
  opacity: 0;
  transition: opacity .3s;
}

.stat-card:hover { border-color: var(--border2); transform: translateY(-2px); }
.stat-card:hover::before { opacity: 1; }

.stat-label {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(120deg, var(--cyan), var(--violet));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-variant-numeric: tabular-nums;
}

.stat-card.today .stat-value { background: linear-gradient(120deg, var(--green), var(--cyan)); -webkit-background-clip: text; background-clip: text; }
.stat-card.week .stat-value  { background: linear-gradient(120deg, var(--violet), #ff7eb3); -webkit-background-clip: text; background-clip: text; }

/* ── ADD FORM ─────────────────────────────────────────────── */
.add-form {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 20px;
  margin-bottom: 20px;
  backdrop-filter: blur(20px);
}

.input-wrap {
  position: relative;
  margin-bottom: 12px;
}

.input-wrap input {
  width: 100%;
  background: rgba(0,0,0,0.35);
  border: 1px solid var(--border2);
  border-radius: 10px;
  padding: 13px 50px 13px 16px;
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}

.input-wrap input:focus {
  border-color: var(--cyan);
  box-shadow: 0 0 0 3px rgba(0,200,255,0.10);
}

.input-wrap input::placeholder { color: var(--muted); }

.char-count {
  position: absolute;
  right: 14px; top: 50%;
  transform: translateY(-50%);
  font-family: var(--mono);
  font-size: 11px;
  color: var(--muted);
  pointer-events: none;
  transition: color .2s;
}

.char-count.warn { color: var(--amber); }
.char-count.over { color: var(--red); }

.form-row {
  display: flex;
  gap: 10px;
}

/* ── BUTTONS ──────────────────────────────────────────────── */
.btn {
  font-family: var(--font);
  font-weight: 700;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  padding: 12px 20px;
  font-size: 13px;
  letter-spacing: 0.5px;
  transition: transform .2s, box-shadow .2s, opacity .2s;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  position: relative;
  overflow: hidden;
}

.btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.12);
  opacity: 0;
  transition: opacity .15s;
}

.btn:hover::after { opacity: 1; }
.btn:hover { transform: translateY(-1px); }
.btn:active { transform: translateY(0) scale(0.97); }

.btn-primary {
  background: linear-gradient(135deg, var(--cyan), #0090cc);
  color: #001a26;
  flex: 1;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0,200,255,0.25);
}

.btn-ghost {
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border2);
  color: var(--muted);
}

.btn-ghost:hover { color: var(--text); border-color: var(--border2); }

.btn-danger {
  background: rgba(255,64,96,0.15);
  border: 1px solid rgba(255,64,96,0.3);
  color: var(--red);
  font-size: 12px;
  padding: 7px 11px;
}

.btn-danger:hover { background: rgba(255,64,96,0.25); }

.btn-edit {
  background: rgba(155,92,255,0.15);
  border: 1px solid rgba(155,92,255,0.3);
  color: var(--violet);
  font-size: 12px;
  padding: 7px 11px;
}

.btn-edit:hover { background: rgba(155,92,255,0.28); }

.btn-sm {
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 8px 14px;
  font-size: 12px;
  border-radius: 8px;
}

/* ── TOOLBAR ──────────────────────────────────────────────── */
.toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.search-wrap {
  flex: 1;
  min-width: 180px;
  position: relative;
}

.search-wrap input {
  width: 100%;
  background: rgba(0,0,0,0.4);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 16px 10px 38px;
  color: var(--text);
  font-family: var(--font);
  font-size: 14px;
  outline: none;
  transition: border-color .2s;
}

.search-wrap input:focus { border-color: var(--cyan); }
.search-wrap input::placeholder { color: var(--muted); }

.search-icon {
  position: absolute;
  left: 12px; top: 50%;
  transform: translateY(-50%);
  color: var(--muted);
  pointer-events: none;
  font-size: 14px;
}

.sort-sel {
  background: rgba(0,0,0,0.4);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 14px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 12px;
  outline: none;
  cursor: pointer;
  transition: border-color .2s;
}

.sort-sel:focus { border-color: var(--cyan); }

/* ── BULK BAR ─────────────────────────────────────────────── */
.bulk-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,64,96,0.08);
  border: 1px solid rgba(255,64,96,0.22);
  border-radius: 10px;
  padding: 10px 16px;
  margin-bottom: 12px;
  transition: all .3s;
}

.bulk-bar.hidden { display: none; }
.bulk-label {
  font-size: 13px;
  color: var(--red);
  font-weight: 600;
  flex: 1;
}

/* ── USER LIST ────────────────────────────────────────────── */
#list { display: flex; flex-direction: column; gap: 8px; }

.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: border-color .25s, transform .25s, box-shadow .25s, opacity .3s;
  cursor: default;
  position: relative;
  overflow: hidden;
  animation: slideIn .35s cubic-bezier(.22,1,.36,1) both;
}

.card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, var(--cyan), var(--violet));
  opacity: 0;
  transition: opacity .3s;
  border-radius: 3px 0 0 3px;
}

.card:hover { border-color: var(--border2); transform: translateX(3px); box-shadow: 0 4px 30px rgba(0,200,255,0.07); }
.card:hover::before { opacity: 1; }

.card.selected {
  border-color: rgba(255,64,96,0.5);
  background: rgba(255,64,96,0.06);
}

.card.selected::before {
  background: linear-gradient(180deg, var(--red), #ff7090);
  opacity: 1;
}

.card.removing {
  animation: slideOut .3s cubic-bezier(.55,0,1,.45) forwards;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}

@keyframes slideOut {
  to { opacity: 0; transform: translateX(20px) scale(0.95); height: 0; padding: 0; margin: 0; }
}

.card-check {
  width: 18px; height: 18px;
  border: 1.5px solid var(--border2);
  border-radius: 5px;
  background: rgba(0,0,0,0.3);
  cursor: pointer;
  flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  transition: background .2s, border-color .2s;
  font-size: 10px;
  color: white;
}

.card-check:hover { border-color: var(--red); }
.card.selected .card-check { background: var(--red); border-color: var(--red); }

.card-avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--cyan), var(--violet));
  display: flex; align-items: center; justify-content: center;
  font-weight: 800;
  font-size: 14px;
  color: var(--bg);
  flex-shrink: 0;
  text-transform: uppercase;
  letter-spacing: -0.5px;
}

.card-body { flex: 1; min-width: 0; }

.card-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
}

.card-name:hover { color: var(--cyan); }

.card-meta {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--muted);
  margin-top: 2px;
}

.card-actions { display: flex; gap: 6px; flex-shrink: 0; }

/* Edit inline input inside card */
.card-edit-input {
  background: rgba(0,0,0,0.4);
  border: 1px solid var(--cyan);
  border-radius: 8px;
  padding: 6px 10px;
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  font-weight: 600;
  outline: none;
  width: 100%;
  box-shadow: 0 0 0 3px rgba(0,200,255,0.1);
}

/* ── EMPTY STATE ──────────────────────────────────────────── */
.empty {
  text-align: center;
  padding: 60px 20px;
  display: none;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 14px;
  opacity: 0.5;
  display: block;
}

.empty p {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 13px;
}

/* ── TOASTS ───────────────────────────────────────────────── */
#toast-root {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  backdrop-filter: blur(20px);
  min-width: 200px;
  max-width: 320px;
  pointer-events: auto;
  animation: toastIn .35s cubic-bezier(.22,1,.36,1) both;
  border: 1px solid transparent;
  cursor: pointer;
}

.toast.out { animation: toastOut .3s ease forwards; }

.toast.success { background: rgba(0,255,178,0.15); border-color: rgba(0,255,178,0.3); color: var(--green); }
.toast.error   { background: rgba(255,64,96,0.15);  border-color: rgba(255,64,96,0.3);  color: var(--red); }
.toast.info    { background: rgba(0,200,255,0.12);  border-color: rgba(0,200,255,0.25); color: var(--cyan); }
.toast.warn    { background: rgba(255,184,0,0.13);  border-color: rgba(255,184,0,0.3);  color: var(--amber); }

@keyframes toastIn {
  from { opacity: 0; transform: translateX(30px) scale(0.92); }
  to   { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes toastOut {
  to   { opacity: 0; transform: translateX(30px) scale(0.9); }
}

/* ── UNDO BAR ─────────────────────────────────────────────── */
.undo-bar {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 13px;
  backdrop-filter: blur(20px);
  z-index: 9998;
  animation: undoIn .35s cubic-bezier(.22,1,.36,1);
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}

.undo-bar.gone { display: none; }

@keyframes undoIn {
  from { opacity: 0; transform: translate(-50%, 20px); }
  to   { opacity: 1; transform: translate(-50%, 0); }
}

.undo-prog {
  position: absolute;
  bottom: 0; left: 0;
  height: 2px;
  background: var(--cyan);
  border-radius: 0 0 12px 12px;
  transition: width linear;
}

.undo-btn {
  font-family: var(--font);
  font-weight: 700;
  color: var(--cyan);
  cursor: pointer;
  background: none;
  border: none;
  font-size: 13px;
  padding: 0;
  text-decoration: underline;
}

/* ── CONTEXT MENU ─────────────────────────────────────────── */
.ctx-menu {
  position: fixed;
  z-index: 9997;
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 12px;
  padding: 6px;
  min-width: 160px;
  backdrop-filter: blur(20px);
  box-shadow: 0 10px 50px rgba(0,0,0,0.6);
  animation: ctxIn .2s cubic-bezier(.22,1,.36,1);
}

@keyframes ctxIn {
  from { opacity: 0; transform: scale(0.92); }
  to   { opacity: 1; transform: scale(1); }
}

.ctx-item {
  padding: 9px 12px;
  border-radius: 7px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background .15s;
  font-weight: 600;
}

.ctx-item:hover { background: rgba(255,255,255,0.07); }
.ctx-item.danger { color: var(--red); }
.ctx-item.accent { color: var(--cyan); }

/* ── KEYBOARD HINTS ───────────────────────────────────────── */
.kbd-hints {
  display: flex;
  gap: 16px;
  margin-top: 18px;
  justify-content: center;
  flex-wrap: wrap;
}

.hint {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 5px;
}

kbd {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 5px;
  padding: 2px 6px;
  font-size: 10px;
  color: var(--text);
}

/* ── DRAG & DROP ──────────────────────────────────────────── */
.card.drag-over { border-color: var(--violet); background: rgba(155,92,255,0.08); }
.card[draggable="true"] { cursor: grab; }
.card[draggable="true"]:active { cursor: grabbing; }

/* ── SCROLLBAR ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,200,255,0.2); border-radius: 10px; }

/* ── SHIMMER LOADING ──────────────────────────────────────── */
.shimmer {
  background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 50%, var(--surface) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

@keyframes shimmer { to { background-position: -200% 0; } }

/* ── EXPORT DROPDOWN ──────────────────────────────────────── */
.export-wrap { position: relative; }

.export-menu {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 10px;
  min-width: 140px;
  overflow: hidden;
  z-index: 100;
  backdrop-filter: blur(20px);
  box-shadow: 0 10px 40px rgba(0,0,0,0.5);
  animation: ctxIn .2s ease;
}

.export-menu.hidden { display: none; }

.export-item {
  padding: 10px 14px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  gap: 8px;
  align-items: center;
  transition: background .15s;
  font-weight: 600;
  color: var(--muted);
}

.export-item:hover { background: rgba(255,255,255,0.06); color: var(--text); }

/* ── RESPONSIVE ───────────────────────────────────────────── */
@media (max-width: 520px) {
  .stats-bar { grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .stat-value { font-size: 22px; }
  .logo-name { font-size: 26px; }
  .toolbar { gap: 8px; }
}
</style>
</head>

<body>

<canvas id="bg-canvas"></canvas>
<div id="toast-root"></div>
<div id="ctx-menu" class="ctx-menu" style="display:none;"></div>

<div class="shell">

  <!-- HEADER -->
  <header>
    <div class="logo">
      <span class="logo-tag">// user registry</span>
      <span class="logo-name">NEXUS</span>
    </div>
    <div class="header-actions">
      <div class="export-wrap">
        <button class="btn btn-ghost btn-sm" onclick="toggleExport(event)">⬇ Export</button>
        <div class="export-menu hidden" id="export-menu">
          <a class="export-item" href="/export?fmt=csv">📄 CSV</a>
          <a class="export-item" href="/export?fmt=json">🗂 JSON</a>
        </div>
      </div>
    </div>
  </header>

  <!-- STATS -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-label">Total</div>
      <div class="stat-value" id="stat-total">…</div>
    </div>
    <div class="stat-card today">
      <div class="stat-label">Today</div>
      <div class="stat-value" id="stat-today">…</div>
    </div>
    <div class="stat-card week">
      <div class="stat-label">This Week</div>
      <div class="stat-value" id="stat-week">…</div>
    </div>
  </div>

  <!-- ADD FORM -->
  <div class="add-form">
    <div class="input-wrap">
      <input id="name-input" maxlength="100" placeholder="Enter user name…"
        oninput="updateChar(this)" onkeydown="handleAddKey(event)" autocomplete="off">
      <span class="char-count" id="char-count">0/100</span>
    </div>
    <div class="form-row">
      <button class="btn btn-primary" id="add-btn" onclick="addUser()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add User
      </button>
    </div>
  </div>

  <!-- BULK BAR -->
  <div class="bulk-bar hidden" id="bulk-bar">
    <span class="bulk-label" id="bulk-label">0 selected</span>
    <button class="btn btn-danger" onclick="bulkDelete()">🗑 Delete selected</button>
    <button class="btn btn-ghost btn-sm" onclick="clearSelection()">✕ Clear</button>
  </div>

  <!-- TOOLBAR -->
  <div class="toolbar">
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input id="search-input" placeholder="Search users…" oninput="filterList(this.value)" autocomplete="off">
    </div>
    <select class="sort-sel" onchange="changeSort(this.value)">
      <option value="id_desc" {% if sort=='id_desc' %}selected{% endif %}>Newest first</option>
      <option value="id_asc"  {% if sort=='id_asc'  %}selected{% endif %}>Oldest first</option>
      <option value="name_asc" {% if sort=='name_asc' %}selected{% endif %}>A → Z</option>
      <option value="name_desc" {% if sort=='name_desc' %}selected{% endif %}>Z → A</option>
    </select>
  </div>

  <!-- LIST -->
  <div id="list">
    {% for row in rows %}
    <div class="card"
         data-id="{{ row.id }}"
         data-name="{{ row.name }}"
         draggable="true"
         oncontextmenu="showCtx(event, {{ row.id }}, '{{ row.name | e }}')"
         ondragstart="dragStart(event)"
         ondragover="dragOver(event)"
         ondrop="dragDrop(event)"
         ondragleave="dragLeave(event)">
      <div class="card-check" onclick="toggleSelect(this.closest('.card'))">✓</div>
      <div class="card-avatar">{{ row.name[0] }}</div>
      <div class="card-body">
        <div class="card-name" ondblclick="startEdit(this.closest('.card'))">{{ row.name }}</div>
        <div class="card-meta">ID #{{ row.id }} · {{ row.created_at.strftime('%b %d, %Y') }}</div>
      </div>
      <div class="card-actions">
        <button class="btn btn-edit" onclick="startEdit(this.closest('.card'))">✎ Edit</button>
        <button class="btn btn-danger" onclick="deleteUser({{ row.id }}, this.closest('.card'))">✕</button>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- EMPTY STATE -->
  <div class="empty" id="empty-state">
    <span class="empty-icon">◎</span>
    <p>No users yet. Add one above.</p>
  </div>

  <!-- KEYBOARD HINTS -->
  <div class="kbd-hints">
    <span class="hint"><kbd>Enter</kbd> add</span>
    <span class="hint"><kbd>Dbl-click</kbd> edit</span>
    <span class="hint"><kbd>Right-click</kbd> menu</span>
    <span class="hint"><kbd>Drag</kbd> reorder</span>
    <span class="hint"><kbd>Esc</kbd> cancel</span>
  </div>

</div><!-- .shell -->

<!-- UNDO BAR template (hidden) -->
<div class="undo-bar gone" id="undo-bar">
  <span id="undo-msg" style="color:var(--muted)"></span>
  <button class="undo-btn" onclick="undoDelete()">Undo</button>
  <div class="undo-prog" id="undo-prog"></div>
</div>

<script>
/* ═══════════════════════════════════════════════════════════
   ANIMATED BACKGROUND CANVAS
═══════════════════════════════════════════════════════════ */
(function() {
  const canvas = document.getElementById("bg-canvas");
  const ctx = canvas.getContext("2d");
  let W, H, pts = [];

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function init() {
    pts = [];
    const count = Math.floor((W * H) / 18000);
    for (let i = 0; i < count; i++) {
      pts.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.5 + 0.4,
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    // Grid
    ctx.strokeStyle = "rgba(0,200,255,0.03)";
    ctx.lineWidth = 1;
    const gs = 80;
    for (let x = 0; x < W; x += gs) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += gs) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    // Particles & lines
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(0,200,255,0.35)";
      ctx.fill();

      for (let j = i + 1; j < pts.length; j++) {
        const q = pts[j];
        const dx = q.x - p.x, dy = q.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(0,200,255,${0.06 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }

  resize();
  init();
  draw();
  window.addEventListener("resize", () => { resize(); init(); });
})();

/* ═══════════════════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════════════════ */
let selectedIds = new Set();
let undoData    = null;
let undoTimer   = null;
let dragSrcId   = null;

/* ═══════════════════════════════════════════════════════════
   STATS
═══════════════════════════════════════════════════════════ */
async function loadStats() {
  const s = await fetch("/stats").then(r => r.json());
  animateNum("stat-total", s.total);
  animateNum("stat-today", s.today);
  animateNum("stat-week",  s.week);
}

function animateNum(id, target) {
  const el = document.getElementById(id);
  const start = parseInt(el.innerText) || 0;
  const dur = 600, t0 = performance.now();
  function step(t) {
    const p = Math.min((t - t0) / dur, 1);
    const v = Math.round(start + (target - start) * easeOut(p));
    el.innerText = v;
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

/* ═══════════════════════════════════════════════════════════
   CHAR COUNT
═══════════════════════════════════════════════════════════ */
function updateChar(inp) {
  const cc = document.getElementById("char-count");
  const n = inp.value.length;
  cc.innerText = `${n}/100`;
  cc.className = "char-count" + (n > 90 ? " over" : n > 70 ? " warn" : "");
}

/* ═══════════════════════════════════════════════════════════
   ADD USER
═══════════════════════════════════════════════════════════ */
async function addUser() {
  const inp = document.getElementById("name-input");
  const name = inp.value.trim();
  if (!name) { toast("Name cannot be empty", "warn"); inp.focus(); return; }

  const btn = document.getElementById("add-btn");
  btn.disabled = true;
  btn.innerHTML = `<span style="opacity:.6">Adding…</span>`;

  const res = await fetch("/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });
  const data = await res.json();
  btn.disabled = false;
  btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> Add User`;

  if (!data.ok) { toast(data.error, "error"); return; }

  const card = buildCard(data.row);
  const list = document.getElementById("list");
  list.prepend(card);
  inp.value = "";
  updateChar(inp);
  checkEmpty();
  loadStats();
  toast(`"${data.row.name}" added`, "success");
}

function buildCard(row) {
  const div = document.createElement("div");
  div.className = "card";
  div.dataset.id   = row.id;
  div.dataset.name = row.name;
  div.draggable    = true;
  div.setAttribute("oncontextmenu", `showCtx(event,${row.id},'${row.name.replace(/'/g,"\\'")}'); return false;`);
  div.setAttribute("ondragstart", "dragStart(event)");
  div.setAttribute("ondragover",  "dragOver(event)");
  div.setAttribute("ondrop",      "dragDrop(event)");
  div.setAttribute("ondragleave", "dragLeave(event)");

  div.innerHTML = `
    <div class="card-check" onclick="toggleSelect(this.closest('.card'))">✓</div>
    <div class="card-avatar">${row.name[0].toUpperCase()}</div>
    <div class="card-body">
      <div class="card-name" ondblclick="startEdit(this.closest('.card'))">${escHtml(row.name)}</div>
      <div class="card-meta">ID #${row.id} · ${row.created_at}</div>
    </div>
    <div class="card-actions">
      <button class="btn btn-edit"   onclick="startEdit(this.closest('.card'))">✎ Edit</button>
      <button class="btn btn-danger" onclick="deleteUser(${row.id}, this.closest('.card'))">✕</button>
    </div>`;
  return div;
}

function handleAddKey(e) {
  if (e.key === "Enter") addUser();
}

/* ═══════════════════════════════════════════════════════════
   DELETE
═══════════════════════════════════════════════════════════ */
async function deleteUser(id, card) {
  const name = card.dataset.name;
  card.classList.add("removing");

  undoData = { id, name, cardHtml: card.outerHTML };
  await fetch(`/delete/${id}`, { method: "DELETE" });

  setTimeout(() => card.remove(), 280);
  checkEmpty();
  loadStats();
  showUndo(name);
  selectedIds.delete(id);
  updateBulkBar();
}

function showUndo(name) {
  clearTimeout(undoTimer);
  const bar  = document.getElementById("undo-bar");
  const prog = document.getElementById("undo-prog");
  const msg  = document.getElementById("undo-msg");

  msg.innerText = `"${name}" deleted`;
  bar.classList.remove("gone");
  prog.style.transition = "none";
  prog.style.width = "100%";

  requestAnimationFrame(() => {
    prog.style.transition = "width 5s linear";
    prog.style.width = "0%";
  });

  undoTimer = setTimeout(() => {
    bar.classList.add("gone");
    undoData = null;
  }, 5000);
}

async function undoDelete() {
  if (!undoData) return;
  clearTimeout(undoTimer);
  document.getElementById("undo-bar").classList.add("gone");

  const res  = await fetch("/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: undoData.name })
  });
  const data = await res.json();
  if (data.ok) {
    const card = buildCard(data.row);
    document.getElementById("list").prepend(card);
    loadStats();
    checkEmpty();
    toast(`Restored "${undoData.name}"`, "success");
  }
  undoData = null;
}

/* ═══════════════════════════════════════════════════════════
   INLINE EDIT
═══════════════════════════════════════════════════════════ */
function startEdit(card) {
  if (card.querySelector(".card-edit-input")) return;
  const nameEl = card.querySelector(".card-name");
  const old    = nameEl.innerText;
  const id     = parseInt(card.dataset.id);

  const inp = document.createElement("input");
  inp.className = "card-edit-input";
  inp.value = old;
  nameEl.replaceWith(inp);
  inp.focus();
  inp.select();

  async function commit() {
    const newName = inp.value.trim();
    if (newName && newName !== old) {
      const res = await fetch(`/edit/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName })
      });
      const d = await res.json();
      if (!d.ok) { toast(d.error, "error"); }
      else {
        card.dataset.name = newName;
        card.querySelector(".card-avatar").innerText = newName[0].toUpperCase();
        toast("Updated", "info");
      }
    }
    const span = document.createElement("div");
    span.className = "card-name";
    span.ondblclick = () => startEdit(card);
    span.innerText = d?.name || newName || old;
    inp.replaceWith(span);
  }

  let d = null;
  inp.addEventListener("blur", commit);
  inp.addEventListener("keydown", e => {
    if (e.key === "Enter")  { inp.blur(); }
    if (e.key === "Escape") { inp.value = old; inp.removeEventListener("blur", commit); const span = document.createElement("div"); span.className = "card-name"; span.ondblclick = () => startEdit(card); span.innerText = old; inp.replaceWith(span); }
  });
}

/* ═══════════════════════════════════════════════════════════
   MULTI SELECT
═══════════════════════════════════════════════════════════ */
function toggleSelect(card) {
  const id = parseInt(card.dataset.id);
  if (selectedIds.has(id)) {
    selectedIds.delete(id);
    card.classList.remove("selected");
  } else {
    selectedIds.add(id);
    card.classList.add("selected");
  }
  updateBulkBar();
}

function clearSelection() {
  selectedIds.clear();
  document.querySelectorAll(".card.selected").forEach(c => c.classList.remove("selected"));
  updateBulkBar();
}

function updateBulkBar() {
  const bar = document.getElementById("bulk-bar");
  if (selectedIds.size > 0) {
    bar.classList.remove("hidden");
    document.getElementById("bulk-label").innerText = `${selectedIds.size} selected`;
  } else {
    bar.classList.add("hidden");
  }
}

async function bulkDelete() {
  if (selectedIds.size === 0) return;
  const ids = [...selectedIds];
  await fetch("/delete-bulk", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ids })
  });
  ids.forEach(id => {
    const card = document.querySelector(`.card[data-id="${id}"]`);
    if (card) { card.classList.add("removing"); setTimeout(() => card.remove(), 280); }
  });
  toast(`Deleted ${ids.length} users`, "warn");
  selectedIds.clear();
  updateBulkBar();
  setTimeout(() => { loadStats(); checkEmpty(); }, 300);
}

/* ═══════════════════════════════════════════════════════════
   FILTER / SORT
═══════════════════════════════════════════════════════════ */
function filterList(q) {
  q = q.toLowerCase();
  let visible = 0;
  document.querySelectorAll(".card").forEach(card => {
    const match = card.dataset.name.toLowerCase().includes(q);
    card.style.display = match ? "" : "none";
    if (match) visible++;
  });
  document.getElementById("empty-state").style.display =
    (visible === 0 && q) ? "block" : "none";
}

function changeSort(val) {
  window.location.href = `/?sort=${val}`;
}

/* ═══════════════════════════════════════════════════════════
   EMPTY STATE
═══════════════════════════════════════════════════════════ */
function checkEmpty() {
  const cards = document.querySelectorAll(".card");
  document.getElementById("empty-state").style.display =
    cards.length === 0 ? "block" : "none";
}

/* ═══════════════════════════════════════════════════════════
   DRAG & DROP REORDER
═══════════════════════════════════════════════════════════ */
function dragStart(e) {
  dragSrcId = e.currentTarget.dataset.id;
  e.dataTransfer.effectAllowed = "move";
}

function dragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add("drag-over");
}

function dragLeave(e) {
  e.currentTarget.classList.remove("drag-over");
}

async function dragDrop(e) {
  e.preventDefault();
  const target = e.currentTarget;
  target.classList.remove("drag-over");
  const srcId = dragSrcId;
  const dstId = target.dataset.id;
  if (srcId === dstId) return;

  const list = document.getElementById("list");
  const src  = list.querySelector(`.card[data-id="${srcId}"]`);
  const dst  = list.querySelector(`.card[data-id="${dstId}"]`);

  if (src && dst) {
    const cards = [...list.children];
    const si = cards.indexOf(src), di = cards.indexOf(dst);
    if (si < di) dst.after(src); else dst.before(src);
  }

  const order = [...list.querySelectorAll(".card")].map(c => parseInt(c.dataset.id));
  await fetch("/reorder", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ order })
  });
  toast("Order saved", "info");
}

/* ═══════════════════════════════════════════════════════════
   CONTEXT MENU
═══════════════════════════════════════════════════════════ */
function showCtx(e, id, name) {
  e.preventDefault();
  const menu = document.getElementById("ctx-menu");
  menu.style.display = "block";
  menu.style.left = `${Math.min(e.clientX, window.innerWidth - 180)}px`;
  menu.style.top  = `${Math.min(e.clientY, window.innerHeight - 160)}px`;
  menu.innerHTML = `
    <div class="ctx-item accent" onclick="startEdit(document.querySelector('.card[data-id=\\"${id}\\"]')); closeCtx()">✎ Edit name</div>
    <div class="ctx-item" onclick="copyToClipboard('${escJs(name)}'); closeCtx()">⎘ Copy name</div>
    <div class="ctx-item" onclick="toggleSelect(document.querySelector('.card[data-id=\\"${id}\\"]')); closeCtx()">☐ Select</div>
    <div class="ctx-item danger" onclick="deleteUser(${id}, document.querySelector('.card[data-id=\\"${id}\\"]')); closeCtx()">✕ Delete</div>
  `;
}

function closeCtx() {
  document.getElementById("ctx-menu").style.display = "none";
}

document.addEventListener("click", closeCtx);
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeCtx();
});

/* ═══════════════════════════════════════════════════════════
   TOASTS
═══════════════════════════════════════════════════════════ */
function toast(msg, type = "success") {
  const icons = { success: "✓", error: "✕", info: "●", warn: "⚠" };
  const root  = document.getElementById("toast-root");
  const el    = document.createElement("div");
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type] || "●"}</span><span>${escHtml(msg)}</span>`;
  el.onclick = () => dismissToast(el);
  root.appendChild(el);
  setTimeout(() => dismissToast(el), 3500);
}

function dismissToast(el) {
  el.classList.add("out");
  setTimeout(() => el.remove(), 300);
}

/* ═══════════════════════════════════════════════════════════
   EXPORT DROPDOWN
═══════════════════════════════════════════════════════════ */
function toggleExport(e) {
  e.stopPropagation();
  document.getElementById("export-menu").classList.toggle("hidden");
}

document.addEventListener("click", () => {
  document.getElementById("export-menu")?.classList.add("hidden");
});

/* ═══════════════════════════════════════════════════════════
   HELPERS
═══════════════════════════════════════════════════════════ */
function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function escJs(s) {
  return String(s).replace(/\\/g,"\\\\").replace(/'/g,"\\'");
}

async function copyToClipboard(text) {
  try { await navigator.clipboard.writeText(text); toast(`Copied "${text}"`, "info"); }
  catch { toast("Copy failed", "error"); }
}

/* ═══════════════════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════════════════ */
window.addEventListener("DOMContentLoaded", () => {
  loadStats();
  checkEmpty();
  // Stagger existing cards
  document.querySelectorAll(".card").forEach((c, i) => {
    c.style.animationDelay = `${i * 40}ms`;
  });
});
</script>

</body>
</html>
"""

if __name__ == "__main__":
    init_db()
    app.run(debug=True)