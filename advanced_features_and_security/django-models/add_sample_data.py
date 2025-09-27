#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/gargarmel/Downloads/ALX/Alx_DjangoLearnLab/django-models')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing"""
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Harper Lee")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="1984", author=author2)
    book3 = Book.objects.create(title="To Kill a Mockingbird", author=author3)
    book4 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Public Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book2, book4)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="John Smith", library=library1)
    librarian2 = Librarian.objects.create(name="Jane Doe", library=library2)
    
    print("Sample data created successfully!")
    print(f"Authors: {Author.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Libraries: {Library.objects.count()}")
    print(f"Librarians: {Librarian.objects.count()}")

if __name__ == "__main__":
    create_sample_data()