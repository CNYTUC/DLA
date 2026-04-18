import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        subcategory TEXT,
        question_text TEXT,
        image_path TEXT,
        difficulty TEXT,
        active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        transcript TEXT,
        total_score REAL,
        grammar_score REAL,
        fluency_score REAL,
        relevance_score REAL,
        vocabulary_score REAL,
        feedback TEXT,
        improved_answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(question_id) REFERENCES questions(id)
    )
    """)

    conn.commit()
    conn.close()

def add_question(category, subcategory, question_text, image_path, difficulty, active):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO questions (category, subcategory, question_text, image_path, difficulty, active)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (category, subcategory, question_text, image_path, difficulty, int(active)))

    conn.commit()
    conn.close()

def get_all_questions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, category, subcategory, question_text, image_path, difficulty, active, created_at
    FROM questions
    ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

def get_active_questions(category=None, subcategory=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT id, category, subcategory, question_text, image_path, difficulty, active
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

def delete_question(question_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()

def update_question(question_id, category, subcategory, question_text, image_path, difficulty, active):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE questions
    SET category = ?, subcategory = ?, question_text = ?, image_path = ?, difficulty = ?, active = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (category, subcategory, question_text, image_path, difficulty, int(active), question_id))

    conn.commit()
    conn.close()

def save_test_result(
    question_id,
    transcript,
    total_score,
    grammar_score,
    fluency_score,
    relevance_score,
    vocabulary_score,
    feedback,
    improved_answer
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO test_results (
        question_id, transcript, total_score, grammar_score, fluency_score,
        relevance_score, vocabulary_score, feedback, improved_answer
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question_id, transcript, total_score, grammar_score, fluency_score,
        relevance_score, vocabulary_score, feedback, improved_answer
    ))

    conn.commit()
    conn.close()