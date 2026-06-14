"""
Authentication module for BizTrack AI
Handles user signup, login, and session management
"""

import sqlite3
import hashlib
from database import get_connection, log_activity

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def signup(name, email, password, role='staff'):
    """Register a new user"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hashed_pw, role))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Email already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def login(email, password):
    """Authenticate user login"""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute('''
        SELECT id, name, email, role FROM users
        WHERE email = ? AND password = ?
    ''', (email, hashed_pw))
    user = cursor.fetchone()
    conn.close()

    if user:
        log_activity(user[0], "Login", f"User {user[1]} logged in")
        return True, {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'role': user[3]
        }
    return False, "Invalid email or password!"

def get_all_users():
    """Get all users (Admin only)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, role, created_at FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_role(user_id, new_role):
    """Update user role"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Delete a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def change_password(user_id, old_password, new_password):
    """Change user password"""
    conn = get_connection()
    cursor = conn.cursor()

    # Verify old password
    hashed_old = hash_password(old_password)
    cursor.execute('SELECT id FROM users WHERE id = ? AND password = ?',
                   (user_id, hashed_old))
    if not cursor.fetchone():
        conn.close()
        return False, "Current password is incorrect!"

    # Update to new password
    hashed_new = hash_password(new_password)
    cursor.execute('UPDATE users SET password = ? WHERE id = ?',
                   (hashed_new, user_id))
    conn.commit()
    conn.close()
    return True, "Password changed successfully!"
