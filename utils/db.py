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
