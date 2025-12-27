import sqlite3
from typing import List, Tuple

def _get_connection(db_path: str):
    return sqlite3.connect(db_path)

def init_db(db_path: str = "reminders.db") -> None:
    conn = _get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL,
                chat_id   INTEGER NOT NULL,
                remind_at TEXT    NOT NULL,
                text      TEXT    NOT NULL,
                done      INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        conn.commit()
    finally:
        conn.close()

def add_reminder(
    user_id: int,
    chat_id: int,
    remind_at: str,
    text: str,
    db_path: str = "reminders.db",
) -> None:
    conn = _get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reminders (user_id, chat_id, remind_at, text, done) "
            "VALUES (?, ?, ?, ?, 0)",
            (user_id, chat_id, remind_at, text),
        )
        conn.commit()
    finally:
        conn.close()

def get_due_reminders(
    now_str: str,
    db_path: str = "reminders.db",
) -> List[Tuple]:
    conn = _get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, user_id, chat_id, remind_at, text "
            "FROM reminders "
            "WHERE done = 0 AND remind_at <= ?",
            (now_str,),
        )
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()

def get_active_reminders(
    user_id: int,
    db_path: str = "reminders.db",
) -> List[Tuple]:
    conn = _get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, remind_at, text "
            "FROM reminders "
            "WHERE user_id = ? AND done = 0 "
            "ORDER BY remind_at",
            (user_id,),
        )
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()

def mark_done(
    reminder_id: int,
    db_path: str = "reminders.db",
) -> None:
    conn = _get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE reminders SET done = 1 WHERE id = ?",
            (reminder_id,),
        )
        conn.commit()
    finally:
        conn.close()
