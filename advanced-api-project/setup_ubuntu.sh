#!/bin/bash

# Advanced API Development with Django REST Framework - Ubuntu Setup Script
# This script sets up the project on Ubuntu/Debian systems

set -e  # Exit on any error

echo "🚀 Setting up Advanced API Development with Django REST Framework on Ubuntu"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "This script should not be run as root. Please run as a regular user."
    exit 1
fi

# Update package list
print_status "Updating package list..."
sudo apt update

# Install Python 3 and pip if not already installed
print_status "Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install additional dependencies
print_status "Installing additional system dependencies..."
sudo apt install -y build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev

# Install Git if not already installed
if ! command -v git &> /dev/null; then
    print_status "Installing Git..."
    sudo apt install -y git
fi

# Install curl if not already installed
if ! command -v curl &> /dev/null; then
    print_status "Installing curl..."
    sudo apt install -y curl
fi

# Navigate to project directory
print_status "Navigating to project directory..."
cd "$(dirname "$0")"

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install project dependencies
print_status "Installing project dependencies..."
pip install -r requirements.txt

# Run Django migrations
print_status "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
print_status "Creating superuser account..."
echo "Creating a superuser account for Django admin access..."
echo "You can use the following credentials or create your own:"
echo "Username: admin"
echo "Email: admin@example.com"
echo "Password: admin123"
echo ""

# Create superuser non-interactively
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully!')
else:
    print('Superuser already exists!')
EOF

# Run tests to verify installation
print_status "Running tests to verify installation..."
python manage.py test api

# Create sample data (optional)
print_status "Creating sample data..."
python manage.py shell << EOF
from api.models import Author, Book

# Create sample authors
authors_data = [
    {'name': 'J.K. Rowling'},
    {'name': 'George Orwell'},
    {'name': 'Harper Lee'},
    {'name': 'F. Scott Fitzgerald'},
    {'name': 'Jane Austen'}
]

for author_data in authors_data:
    author, created = Author.objects.get_or_create(name=author_data['name'])
    if created:
        print(f'Created author: {author.name}')

# Create sample books
books_data = [
    {'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author_name': 'J.K. Rowling', 'isbn': '9780747532699'},
    {'title': '1984', 'publication_year': 1949, 'author_name': 'George Orwell', 'isbn': '9780451524935'},
    {'title': 'To Kill a Mockingbird', 'publication_year': 1960, 'author_name': 'Harper Lee', 'isbn': '9780061120084'},
    {'title': 'The Great Gatsby', 'publication_year': 1925, 'author_name': 'F. Scott Fitzgerald', 'isbn': '9780743273565'},
    {'title': 'Pride and Prejudice', 'publication_year': 1813, 'author_name': 'Jane Austen', 'isbn': '9780141439518'}
]

for book_data in books_data:
    author = Author.objects.get(name=book_data['author_name'])
    book, created = Book.objects.get_or_create(
        title=book_data['title'],
        author=author,
        defaults={
            'publication_year': book_data['publication_year'],
            'isbn': book_data['isbn']
        }
    )
    if created:
        print(f'Created book: {book.title} by {book.author.name}')
EOF

print_success "Setup completed successfully!"
echo ""
echo "🎉 Advanced API Development Project is ready!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start the development server: python manage.py runserver"
echo "3. Visit http://localhost:8000/api/ to see the API"
echo "4. Visit http://localhost:8000/admin/ to access Django admin"
echo "5. Use username 'admin' and password 'admin123' for admin access"
echo ""
echo "🔧 Available API endpoints:"
echo "• GET  /api/                    - API root with navigation"
echo "• GET  /api/authors/            - List all authors"
echo "• GET  /api/books/               - List all books"
echo "• GET  /api/statistics/          - Get statistics"
echo "• GET  /api/authors/{id}/books/  - Get books by author"
echo ""
echo "🧪 Run tests: python manage.py test api"
echo "📚 Read README.md for detailed documentation"
echo ""
print_success "Happy coding! 🚀"