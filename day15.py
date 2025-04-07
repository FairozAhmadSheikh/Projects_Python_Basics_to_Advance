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
# Add book
def add_book(title, author, genre, year):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, genre, year, added_on) VALUES (?, ?, ?, ?, ?)",
                (title, author, genre, year, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
# Delete book
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
# Fetch all books
def fetch_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()
    return books
# GUI Class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x500")

        self.setup_ui()
        self.refresh_table()
