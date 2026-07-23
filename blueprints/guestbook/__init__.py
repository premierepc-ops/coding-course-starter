import sqlite3
from site_paths import db_path
from flask import Blueprint, render_template, request

DB_PATH = db_path("guestbook.db")


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


guestbook_bp = Blueprint("guestbook", __name__, template_folder="templates")
init_db()


@guestbook_bp.route("/")
def index():
    db = get_db()
    messages = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 20").fetchall()
    db.close()
    return render_template("guestbook/index.html", messages=messages)


@guestbook_bp.route("/messages", methods=["POST"])
def post_message():
    author = request.form.get("author", "").strip()[:80]
    message = request.form.get("message", "").strip()[:500]
    if author and message:
        db = get_db()
        db.execute("INSERT INTO messages (author, message) VALUES (?, ?)", (author, message))
        db.commit()
        db.close()
    db = get_db()
    messages = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 20").fetchall()
    db.close()
    return render_template("guestbook/_messages.html", messages=messages)
