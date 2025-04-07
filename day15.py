import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
# Database setup
def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            year INTEGER,
            added_on TEXT
        )
    """)
    conn.commit()
    conn.close()