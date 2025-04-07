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

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Entry fields
        tk.Label(self.frame, text="Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Author:").grid(row=0, column=2)
        self.author_entry = tk.Entry(self.frame)
        self.author_entry.grid(row=0, column=3)

        tk.Label(self.frame, text="Genre:").grid(row=1, column=0)
        self.genre_entry = tk.Entry(self.frame)
        self.genre_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Year:").grid(row=1, column=2)
        self.year_entry = tk.Entry(self.frame)
        self.year_entry.grid(row=1, column=3)

        # Buttons
        tk.Button(self.frame, text="Add Book", command=self.add_book).grid(row=2, column=1, pady=10)
        tk.Button(self.frame, text="Delete Selected", command=self.delete_selected).grid(row=2, column=2)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Author", "Genre", "Year", "Added"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in fetch_books():
            self.tree.insert("", "end", values=book)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()

        if not title or not author or not year:
            messagebox.showwarning("Input Error", "Title, Author, and Year are required!")
            return

        try:
            int(year)
        except ValueError:
            messagebox.showerror("Invalid Input", "Year must be an integer.")
            return

        add_book(title, author, genre, int(year))
        self.refresh_table()
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            book_id = self.tree.item(item)['values'][0]
            delete_book(book_id)
        self.refresh_table()

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
