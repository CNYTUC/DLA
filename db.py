import sqlite3
from pathlib import Path

DB_PATH = Path("data/db.sqlite3")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def get_all_questions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, category, subcategory, question_text, image_path, active
    FROM questions
    ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def add_question(category, subcategory, question_text, image_path=None, active=True):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO questions
    (category, subcategory, question_text, image_path, active)
    VALUES (?, ?, ?, ?, ?)
    """, (
        category,
        subcategory,
        question_text,
        image_path,
        int(active)
    ))

    conn.commit()
    conn.close()


def delete_question(question_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()


def update_question(question_id, category, subcategory, question_text, image_path, active):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE questions
    SET category = ?,
        subcategory = ?,
        question_text = ?,
        image_path = ?,
        active = ?
    WHERE id = ?
    """, (
        category,
        subcategory,
        question_text,
        image_path,
        int(active),
        question_id
    ))

    conn.commit()
    conn.close()


def get_active_questions(category=None, subcategory=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT id, category, subcategory, question_text, image_path, active
    FROM questions
    WHERE active = 1
    """

    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if subcategory:
        query += " AND subcategory = ?"
        params.append(subcategory)

    query += " ORDER BY RANDOM()"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return rows