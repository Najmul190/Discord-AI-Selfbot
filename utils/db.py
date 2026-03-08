import sqlite3
from utils.helpers import resource_path

db_path = "config/bot_data.db"


def init_db():
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ignored_users (
            id INTEGER PRIMARY KEY
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS convo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def add_channel(channel_id):
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO channels (id) VALUES (?)", (channel_id,))
    conn.commit()
    conn.close()


def remove_channel(channel_id):
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()


def get_channels():
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM channels")
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    return channels


def add_ignored_user(user_id):
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO ignored_users (id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def remove_ignored_user(user_id):
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ignored_users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_ignored_users():
    conn = sqlite3.connect(resource_path(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ignored_users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users


def sv_c(u, c, r, t):
    cx = sqlite3.connect(resource_path(db_path))
    cu = cx.cursor()
    cu.execute("INSERT INTO convo (user_id, channel_id, role, content) VALUES (?, ?, ?, ?)", (u, c, r, t))
    cx.commit()
    cx.close()


def gt_c(u, c, m):
    cx = sqlite3.connect(resource_path(db_path))
    cu = cx.cursor()
    cu.execute("SELECT role, content FROM convo WHERE user_id = ? AND channel_id = ? ORDER BY id DESC LIMIT ?", (u, c, m))
    ms = [{"role": x[0], "content": x[1]} for x in cu.fetchall()]
    cx.close()
    return ms[::-1]


def ck_d(u, c, t):
    cx = sqlite3.connect(resource_path(db_path))
    cu = cx.cursor()
    cu.execute("SELECT COUNT(*) FROM convo WHERE user_id = ? AND channel_id = ? AND role = ? AND content = ?", (u, c, "user", t))
    c = cu.fetchone()[0]
    cx.close()
    return c > 0


def cl_c(u, c):
    cx = sqlite3.connect(resource_path(db_path))
    cu = cx.cursor()
    cu.execute("DELETE FROM convo WHERE user_id = ? AND channel_id = ?", (u, c))
    cx.commit()
    cx.close()


def cl_a():
    cx = sqlite3.connect(resource_path(db_path))
    cu = cx.cursor()
    cu.execute("DELETE FROM convo")
    cx.commit()
    cx.close()
