from flask import Flask, request, render_template_string, jsonify
import pymysql
import time

app = Flask(__name__)

DB_HOST = '172.17.0.2' #mysql-image after running mysql container inspecting it to get ip
DB_USER = "root"
DB_PASSWORD = 'Shubham@6024'
DB_NAME = 'testdb'


def get_conn():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, cursorclass=pymysql.cursors.DictCursor
    )


def init_db():
    while True:
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL
                    )
                """)
                cur.execute("""
                    SELECT COUNT(*) AS cnt FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'created_at'
                """, (DB_NAME,))
                row = cur.fetchone()
                if row['cnt'] == 0:
                    cur.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                    print("Migration: added created_at column.")
            conn.commit()
            conn.close()
            break
        except pymysql.err.OperationalError:
            print("Waiting for MySQL to be ready...")
            time.sleep(2)


init_db()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Registry</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #fffbf5;
            --surface: #ffffff;
            --border: #ede8df;
            --accent: #ff6b35;
            --text: #1a1a2e;
            --muted: #a0a0a0;
            --success: #06d6a0;
            --error: #ef476f;
            --mono: 'JetBrains Mono', monospace;
            --sans: 'Nunito', sans-serif;
        }
        body {
            font-family: var(--sans);
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 28px 20px;
            position: relative;
            overflow-x: hidden;
        }
        body::before {
            content: '';
            position: fixed;
            width: 500px; height: 500px;
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
            z-index: 0;
            background: radial-gradient(circle, rgba(255,210,63,0.30), transparent 70%);
            top: -120px; right: -100px;
        }
        body::after {
            content: '';
            position: fixed;
            width: 400px; height: 400px;
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
            z-index: 0;
            background: radial-gradient(circle, rgba(6,214,160,0.20), transparent 70%);
            bottom: -100px; left: -80px;
        }
        .wrapper { position: relative; z-index: 1; width: 100%; max-width: 620px; }
        header { margin-bottom: 28px; }
        .eyebrow {
            font-family: var(--mono);
            font-size: 11px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 6px;
        }
        h1 { font-size: clamp(30px, 6vw, 46px); font-weight: 900; letter-spacing: -0.02em; }
        h1 span { color: var(--accent); }
        .subtitle { margin-top: 6px; color: var(--muted); font-size: 13px; font-family: var(--mono); }
        .stats-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
        .stat-card { border-radius: 18px; padding: 18px 20px; border: 2px solid transparent; }
        .stat-card:nth-child(1) { background: linear-gradient(135deg,#fff3e0,#ffe5c8); border-color: #ffcc80; }
        .stat-card:nth-child(2) { background: linear-gradient(135deg,#e0f7fa,#c8f0f5); border-color: #80deea; }
        .stat-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); margin-bottom: 4px; }
        .stat-value { font-size: 30px; font-weight: 900; }
        .card { background: var(--surface); border: 2px solid var(--border); border-radius: 20px; padding: 24px; margin-bottom: 14px; box-shadow: 0 4px 24px rgba(0,0,0,0.05); }
        .form-label { display: block; font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }
        .input-row { display: flex; gap: 10px; }
        input[type="text"] {
            flex: 1; padding: 12px 16px;
            background: #fdf8f2; border: 2px solid var(--border);
            border-radius: 12px; color: var(--text);
            font-family: var(--sans); font-size: 15px; font-weight: 600;
            outline: none; transition: border-color 0.2s, box-shadow 0.2s;
        }
        input[type="text"]:focus { border-color: var(--accent); box-shadow: 0 0 0 4px rgba(255,107,53,0.12); background: #fff; }
        input[type="text"]::placeholder { color: #ccc; font-weight: 400; }
        button {
            padding: 12px 22px; background: var(--accent); color: #fff;
            border: none; border-radius: 12px;
            font-family: var(--sans); font-size: 15px; font-weight: 800;
            cursor: pointer; white-space: nowrap;
            box-shadow: 0 4px 14px rgba(255,107,53,0.28);
            transition: background 0.18s, transform 0.1s, box-shadow 0.2s;
        }
        button:hover { background: #e85520; box-shadow: 0 6px 20px rgba(255,107,53,0.38); }
        button:active { transform: scale(0.96); }
        #toast { display: none; margin-top: 12px; padding: 10px 16px; border-radius: 10px; font-family: var(--mono); font-size: 13px; font-weight: 500; animation: slideIn 0.28s ease; }
        #toast.success { background: #e8fdf5; color: #059669; border: 2px solid #a7f3d0; }
        #toast.error   { background: #fff0f3; color: #e63057; border: 2px solid #fecdd3; }
        @keyframes slideIn { from { opacity:0; transform:translateY(-5px); } to { opacity:1; transform:translateY(0); } }
        .list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
        .list-title { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); }
        .search-input {
            padding: 7px 12px; background: #fdf8f2; border: 2px solid var(--border);
            border-radius: 10px; color: var(--text); font-family: var(--sans);
            font-size: 13px; font-weight: 600; outline: none; width: 150px; transition: border-color 0.2s;
        }
        .search-input:focus { border-color: #118ab2; }
        .search-input::placeholder { color: #ccc; font-weight: 400; }
        .user-list { display: flex; flex-direction: column; gap: 8px; }
        .user-item {
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 14px; background: #fdf8f2;
            border: 2px solid var(--border); border-radius: 14px;
            transition: border-color 0.2s, transform 0.15s, box-shadow 0.2s;
            animation: fadeUp 0.3s ease both;
        }
        .user-item:hover { border-color: var(--accent); transform: translateX(4px); box-shadow: 0 3px 14px rgba(255,107,53,0.10); }
        @keyframes fadeUp { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
        .user-info { display: flex; align-items: center; gap: 12px; }
        .avatar { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:15px; color:#fff; flex-shrink:0; }
        .user-name { font-size: 15px; font-weight: 700; }
        .user-meta { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-top: 1px; }
        .user-id { font-family: var(--mono); font-size: 11px; color: var(--muted); background: var(--border); padding: 3px 8px; border-radius: 6px; }
        .delete-btn { background:none; border:2px solid transparent; color:#ccc; padding:5px 10px; border-radius:8px; font-size:13px; cursor:pointer; transition:all 0.18s; box-shadow:none; font-family:var(--mono); font-weight:600; }
        .delete-btn:hover { border-color:var(--error); color:var(--error); background:#fff0f3; box-shadow:none; }
        .empty-state { text-align:center; padding:40px 20px; color:var(--muted); font-size:14px; font-weight:600; }
        .empty-state .icon { font-size:36px; margin-bottom:10px; }
    </style>
</head>
<body>
<div class="wrapper">
    <header>
        <p class="eyebrow">MySQL · Flask · Python</p>
        <h1>User <span>Registry</span></h1>
        <p class="subtitle">// manage your database records</p>
    </header>
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-label">Total Users</div>
            <div class="stat-value" id="total-count">{{ users|length }}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Latest Entry</div>
            <div class="stat-value" style="font-size:17px;padding-top:5px;" id="latest-name">{{ users[0].name if users else '—' }}</div>
        </div>
    </div>
    <div class="card">
        <label class="form-label">Add new user</label>
        <div class="input-row">
            <input type="text" id="name-input" placeholder="Enter name…" maxlength="100" autocomplete="off">
            <button onclick="addUser()">+ Add</button>
        </div>
        <div id="toast"></div>
    </div>
    <div class="card">
        <div class="list-header">
            <span class="list-title">All Users</span>
            <input class="search-input" type="text" id="search" placeholder="Filter…" oninput="filterUsers()">
        </div>
        <div class="user-list" id="user-list">
            {% set colors = ['#ff6b35','#ffd23f','#06d6a0','#118ab2','#ef476f','#9b5de5'] %}
            {% for user in users %}
            <div class="user-item" data-name="{{ user.name.lower() }}" data-id="{{ user.id }}">
                <div class="user-info">
                    <div class="avatar" style="background:{{ colors[loop.index0 % 6] }}">{{ user.name[0].upper() }}</div>
                    <div>
                        <div class="user-name">{{ user.name }}</div>
                        <div class="user-meta">{{ user.created_at.strftime('%b %d, %Y · %H:%M') if user.created_at else '—' }}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <span class="user-id">#{{ user.id }}</span>
                    <button class="delete-btn" onclick="deleteUser({{ user.id }}, this)">✕</button>
                </div>
            </div>
            {% else %}
            <div class="empty-state" id="empty-msg">
                <div class="icon">🌱</div>
                No users yet. Add one above!
            </div>
            {% endfor %}
        </div>
    </div>
</div>
<script>
    const COLORS = ['#ff6b35','#ffd23f','#06d6a0','#118ab2','#ef476f','#9b5de5'];
    let userCount = parseInt(document.getElementById('total-count').textContent);

    function showToast(msg, type) {
        const t = document.getElementById('toast');
        t.textContent = msg; t.className = type; t.style.display = 'block';
        clearTimeout(t._timer);
        t._timer = setTimeout(() => { t.style.display = 'none'; }, 3000);
    }

    async function addUser() {
        const input = document.getElementById('name-input');
        const name = input.value.trim();
        if (!name) { showToast('Please enter a name.', 'error'); return; }
        const res = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        const data = await res.json();
        if (data.success) {
            showToast('✓ ' + name + ' added!', 'success');
            input.value = '';
            prependUser(data.user);
            userCount++;
            document.getElementById('total-count').textContent = userCount;
            document.getElementById('latest-name').textContent = name;
            document.getElementById('empty-msg')?.remove();
        } else {
            showToast('Error: ' + data.error, 'error');
        }
    }

    function prependUser(user) {
        const list = document.getElementById('user-list');
        const color = COLORS[userCount % 6];
        const div = document.createElement('div');
        div.className = 'user-item';
        div.dataset.name = user.name.toLowerCase();
        div.dataset.id = user.id;
        div.innerHTML = `
            <div class="user-info">
                <div class="avatar" style="background:${color}">${user.name[0].toUpperCase()}</div>
                <div>
                    <div class="user-name">${user.name}</div>
                    <div class="user-meta">${user.created_at || '—'}</div>
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span class="user-id">#${user.id}</span>
                <button class="delete-btn" onclick="deleteUser(${user.id}, this)">✕</button>
            </div>`;
        list.prepend(div);
    }

    async function deleteUser(id, btn) {
        const item = btn.closest('.user-item');
        const res = await fetch('/api/users/' + id, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            item.style.transition = 'opacity 0.25s, transform 0.25s';
            item.style.opacity = '0'; item.style.transform = 'translateX(20px)';
            setTimeout(() => { item.remove(); userCount--; document.getElementById('total-count').textContent = userCount; }, 260);
        } else {
            showToast('Delete failed.', 'error');
        }
    }

    function filterUsers() {
        const q = document.getElementById('search').value.toLowerCase();
        document.querySelectorAll('.user-item').forEach(item => {
            item.style.display = item.dataset.name.includes(q) ? '' : 'none';
        });
    }

    document.getElementById('name-input').addEventListener('keydown', e => {
        if (e.key === 'Enter') addUser();
    });
</script>
</body>
</html>
"""


@app.route('/')
def home():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, created_at FROM users ORDER BY id DESC")
        users = cur.fetchall()
    conn.close()
    return render_template_string(HTML, users=users)


@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(success=False, error='Name is required'), 400
    if len(name) > 255:
        return jsonify(success=False, error='Name too long'), 400
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users(name) VALUES(%s)", (name,))
            conn.commit()
            user_id = cur.lastrowid
            cur.execute("SELECT id, name, created_at FROM users WHERE id=%s", (user_id,))
            user = cur.fetchone()
        conn.close()
        user['created_at'] = user['created_at'].strftime('%b %d, %Y · %H:%M') if user.get('created_at') else ''
        return jsonify(success=True, user=user)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)