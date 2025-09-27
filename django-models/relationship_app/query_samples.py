"""
Sample queries demonstrating Django ORM relationships:
- ForeignKey relationships
- ManyToMany relationships  
- OneToOne relationships
"""

from django.db import models
from .models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """
    Query all books by a specific author using ForeignKey relationship.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using related_name='books'
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

def query_books_in_library(library_name):
    """
    List all books in a library using ManyToMany relationship.
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using related_name='libraries'
        return books
    except Library.DoesNotExist:
        return Book.objects.none()

def query_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library using OneToOne relationship.
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using related_name='librarian'
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None

# Example usage functions
def demonstrate_queries():
    """
    Demonstrate all relationship queries with sample data.
    """
    print("=== Django ORM Relationship Queries Demo ===\n")
    
    # Query books by author
    print("1. Books by Author:")
    books_by_author = query_books_by_author("J.K. Rowling")
    for book in books_by_author:
        print(f"   - {book.title}")
    
    print("\n2. Books in Library:")
    books_in_library = query_books_in_library("Central Library")
    for book in books_in_library:
        print(f"   - {book.title} by {book.author.name}")
    
    print("\n3. Librarian for Library:")
    librarian = query_librarian_for_library("Central Library")
    if librarian:
        print(f"   - Librarian: {librarian.name}")
    else:
        print("   - No librarian found")

# Additional relationship queries
def get_author_books_count(author_name):
    """
    Get the count of books by an author.
    """
    try:
        author = Author.objects.get(name=author_name)
        return author.books.count()
    except Author.DoesNotExist:
        return 0

def get_library_books_count(library_name):
    """
    Get the count of books in a library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.count()
    except Library.DoesNotExist:
        return 0

def get_libraries_with_book(book_title):
    """
    Get all libraries that have a specific book.
    """
    try:
        book = Book.objects.get(title=book_title)
        return book.libraries.all()
    except Book.DoesNotExist:
        return Library.objects.none()