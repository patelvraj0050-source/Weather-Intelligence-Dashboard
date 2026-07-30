import sqlite3
from pathlib import Path

DB_FILE = (
    Path(__file__).resolve().parent
    / "weather.db"
)


def get_connection():
    return sqlite3.connect(DB_FILE)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            UNIQUE(city, country)
        )
    """)

    conn.commit()
    conn.close()

def save_search(city, country):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO search_history (city, country)
        VALUES (?, ?)
        """,
        (city, country),
    )

    conn.commit()
    conn.close()

def get_recent_searches(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT city, country, searched_at
        FROM search_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

def add_favorite(city, country):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO favorite_cities (city, country)
        VALUES (?, ?)
        """,
        (city, country),
    )

    conn.commit()
    conn.close()

def get_favorites():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, country
        FROM favorite_cities
        ORDER BY city
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows