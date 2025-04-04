import sqlite3
DATABASE='instance/passwords.db'
# This file contains functions to interact with the SQLite database.
# It includes functions to query data and set data in the database.
# The database is used to store user passwords securely.
# The database is initialized with a table for users if it doesn't exist.

def query_get(query):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def query_set(query):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def init_db():
        query_set("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
