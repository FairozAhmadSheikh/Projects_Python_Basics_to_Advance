import datetime

class Book:
    """Represents a book in the library"""
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {'Available' if self.is_available else 'Checked Out'}"

class Member:
    """Represents a library member"""
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available:
            book.is_available = False
            self.borrowed_books.append((book, datetime.datetime.now()))
            print(f"{self.name} borrowed {book.title}.")
        else:
            print(f"Sorry, {book.title} is currently unavailable.")

    def return_book(self, book):
        for borrowed_book, _ in self.borrowed_books:
            if borrowed_book == book:
                book.is_available = True
                self.borrowed_books.remove((borrowed_book, _))
                print(f"{self.name} returned {book.title}.")
                return
        print(f"{self.name} does not have {book.title}.")

    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id}), Borrowed Books: {len(self.borrowed_books)}"

class Library:
    """Library system managing books and members"""
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added book: {book.title}")

    def add_member(self, member):
        self.members.append(member)
        print(f"Added member: {member.name}")

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def list_books(self):
        return [str(book) for book in self.books]

# Example Usage
if __name__ == "__main__":
    lib = Library()
    
    book1 = Book("1984", "George Orwell", "1234567890")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")
    
    # lib.add_book(book1)
    # lib.add_book(book2)
    
    # member1 = Member("Alice", 1)
    # lib.add_member(member1)
    
    # member1.borrow_book(book1)
    # print(book1)
    
    # member1.return_book(book1)
    # print(book1)
    
    # print("Library Books:", lib.list_books())
