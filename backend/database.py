"""
Database setup and connection management for Diet & Health App.
Uses SQLite with Row factory for dict-like access.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "diet_app.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        height REAL,
        weight REAL,
        food_preference TEXT DEFAULT 'Veg',
        allergies TEXT DEFAULT '[]',
        health_goals TEXT DEFAULT 'General Health',
        medications TEXT DEFAULT '',
        activity_level TEXT DEFAULT 'moderate',
        theme_preference TEXT DEFAULT 'light',
        reset_token TEXT,
        created_at TEXT,
        updated_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS health_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symptoms TEXT DEFAULT '[]',
        bmi REAL,
        bmi_category TEXT,
        deficiencies TEXT DEFAULT '[]',
        health_condition TEXT,
        health_score INTEGER DEFAULT 0,
        recommended_foods TEXT DEFAULT '[]',
        foods_to_avoid TEXT DEFAULT '[]',
        lifestyle_advice TEXT DEFAULT '[]',
        supplement_suggestions TEXT DEFAULT '[]',
        blood_pressure TEXT,
        blood_sugar REAL,
        hemoglobin REAL,
        urgency_level TEXT DEFAULT 'low',
        see_doctor INTEGER DEFAULT 0,
        see_doctor_reason TEXT DEFAULT '',
        combined_diagnosis TEXT,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS diet_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        food_preference TEXT,
        allergies TEXT DEFAULT '[]',
        goal TEXT,
        calories_target INTEGER DEFAULT 2000,
        meal_plan TEXT DEFAULT '{}',
        macros TEXT DEFAULT '{}',
        shopping_list TEXT DEFAULT '[]',
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS routines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        wake_time TEXT DEFAULT '07:00',
        sleep_time TEXT DEFAULT '23:00',
        morning_tasks TEXT DEFAULT '[]',
        afternoon_tasks TEXT DEFAULT '[]',
        evening_tasks TEXT DEFAULT '[]',
        night_tasks TEXT DEFAULT '[]',
        medications TEXT DEFAULT '[]',
        exercise_type TEXT DEFAULT 'general',
        exercise_plan TEXT DEFAULT '{}',
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        water_glasses INTEGER DEFAULT 0,
        exercise_done INTEGER DEFAULT 0,
        meals_followed INTEGER DEFAULT 0,
        weight REAL,
        mood TEXT DEFAULT 'neutral',
        energy_level INTEGER DEFAULT 5,
        notes TEXT DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        body TEXT,
        reminder_time TEXT,
        repeat_type TEXT DEFAULT 'daily',
        category TEXT DEFAULT 'other',
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")
    migrate_db()

def migrate_db():
    conn = get_connection()
    cursor = conn.cursor()
    columns_to_add = [
        ("body", "TEXT"),
        ("repeat_type", "TEXT DEFAULT 'daily'"),
        ("category", "TEXT DEFAULT 'other'"),
        ("is_active", "INTEGER DEFAULT 1")
    ]
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(
                f"ALTER TABLE reminders ADD COLUMN {col_name} {col_type}"
            )
            conn.commit()
            print(f"Added column: {col_name}")
        except Exception as e:
            pass
    conn.close()

# Auto-init on import
init_db()
migrate_db()
