from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlite3
import os

class User(UserMixin):
    def __init__(self, id: int, username: str, password_hash: str):
        self.id = id
        self.username = username
        self.password_hash = password_hash

class AuthManager:
    def __init__(self, db_path: str = 'users.db'):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize the users database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
    def create_user(self, username: str, password: str, role: str = 'user') -> bool:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
            
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        conn.close()
        
        if user_data:
            return User(*user_data)
        return None
        
    def verify_password(self, username: str, password: str) -> bool:
        """Verify user password"""
        user = self.get_user(username)
        if user:
            return check_password_hash(user.password_hash, password)
        return False 