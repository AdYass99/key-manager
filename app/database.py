import sqlite3
from flask import current_app
import os

def query_get(query):
    DATABASE_PATH = current_app.config['DATABASE_PATH']
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def query_set(query):
    DATABASE_PATH = current_app.config['DATABASE_PATH']
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def init_db():
    DATABASE_PATH = current_app.config['DATABASE_PATH']
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    # Crear tabla de usuarios
    query_set("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            master_password_hash TEXT NOT NULL
        )
    """)
        
    query_set("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_name TEXT NOT NULL,
            password TEXT,
            salt TEXT,
            nonce TEXT,
            tag TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
