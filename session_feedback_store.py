"""Persist per-step session feedback for curriculum improvement."""

import sqlite3
from typing import Optional

from site_paths import db_path

DB_PATH = db_path("session_feedback.db")


def get_db():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS session_step_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_num INTEGER NOT NULL,
            step_num INTEGER NOT NULL,
            learner_slug TEXT NOT NULL DEFAULT '',
            author_role TEXT NOT NULL,
            author_name TEXT NOT NULL DEFAULT '',
            worked TEXT NOT NULL DEFAULT '',
            didnt_work TEXT NOT NULL DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    db.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_session_step_feedback_lookup
        ON session_step_feedback (session_num, step_num, created_at DESC)
        """
    )
    db.commit()
    db.close()


init_db()


def save_feedback(
    *,
    session_num: int,
    step_num: int,
    learner_slug: str,
    author_role: str,
    author_name: str,
    worked: str,
    didnt_work: str,
) -> None:
    db = get_db()
    db.execute(
        """
        INSERT INTO session_step_feedback
            (session_num, step_num, learner_slug, author_role, author_name, worked, didnt_work)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_num,
            step_num,
            (learner_slug or "").strip(),
            author_role,
            (author_name or "").strip(),
            worked.strip(),
            didnt_work.strip(),
        ),
    )
    db.commit()
    db.close()


def list_feedback(session_num: Optional[int] = None, step_num: Optional[int] = None, limit: int = 200):
    db = get_db()
    query = "SELECT * FROM session_step_feedback WHERE 1=1"
    params: list = []
    if session_num is not None:
        query += " AND session_num = ?"
        params.append(session_num)
    if step_num is not None:
        query += " AND step_num = ?"
        params.append(step_num)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = db.execute(query, params).fetchall()
    db.close()
    return rows


def feedback_counts(session_num: int) -> dict[int, int]:
    db = get_db()
    rows = db.execute(
        """
        SELECT step_num, COUNT(*) AS n
        FROM session_step_feedback
        WHERE session_num = ?
        GROUP BY step_num
        """,
        (session_num,),
    ).fetchall()
    db.close()
    return {row["step_num"]: row["n"] for row in rows}


def recent_for_step(session_num: int, step_num: int, limit: int = 3):
    return list_feedback(session_num=session_num, step_num=step_num, limit=limit)


def summary_by_session():
    """Grouped counts + latest entry per session/step for instructor review."""
    db = get_db()
    rows = db.execute(
        """
        SELECT session_num, step_num, COUNT(*) AS entry_count,
               MAX(created_at) AS latest_at
        FROM session_step_feedback
        GROUP BY session_num, step_num
        ORDER BY session_num, step_num
        """
    ).fetchall()
    db.close()
    return rows
