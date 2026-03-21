"""
User Service - Database logic for user management using SQLite
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserService:
    def __init__(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, "diet_app.db")
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def register(self, name, email, password, age=None, gender=None):
        """Register a new user with hashed password."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return {"success": False, "message": "Email already registered."}

            hashed_password = generate_password_hash(password)
            created_at = datetime.utcnow().isoformat()
            
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, age, gender, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, hashed_password, age, gender, created_at))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {"success": True, "user_id": user_id, "message": "Registration successful."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def login(self, email, password):
        """Authenticate user and return user info as a 'token'."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            return {
                "success": True, 
                "token": f"{user['id']}:{user['email']}", 
                "user": {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email']
                },
                "message": "Login successful."
            }
        return {"success": False, "message": "Invalid email or password."}

    def get_profile(self, identifier):
        """Fetch user profile by ID or email (identifier)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if ":" in identifier: # token format id:email
            uid = identifier.split(":")[0]
            cursor.execute("SELECT * FROM users WHERE id = ?", (uid,))
        else:
            cursor.execute("SELECT * FROM users WHERE email = ?", (identifier,))
            
        user = cursor.fetchone()
        conn.close()

        if user:
            return {
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "age": user['age'],
                "gender": user['gender'],
                "created_at": user['created_at']
            }
        return None
