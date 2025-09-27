#!/usr/bin/env python3
"""
Advanced API Development with Django REST Framework - Cross-Platform Setup Script
This script sets up the project on both Windows and Unix-like systems
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Colors for output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Print colored output"""
    print(f"{color}{message}{Colors.END}")

def print_status(message):
    """Print status message"""
    print_colored(f"[INFO] {message}", Colors.BLUE)

def print_success(message):
    """Print success message"""
    print_colored(f"[SUCCESS] {message}", Colors.GREEN)

def print_warning(message):
    """Print warning message"""
    print_colored(f"[WARNING] {message}", Colors.YELLOW)

def print_error(message):
    """Print error message"""
    print_colored(f"[ERROR] {message}", Colors.RED)

def run_command(command, check=True, shell=True):
    """Run a command and return the result"""
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, shell=shell, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Command failed: {command}")
            print_error(f"Error: {e.stderr}")
            sys.exit(1)
        return e

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8+ is required")
        print_error(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print_success(f"Python {version.major}.{version.minor}.{version.micro} is compatible")

def check_pip():
    """Check if pip is available"""
    try:
        result = run_command([sys.executable, "-m", "pip", "--version"], check=False)
        if result.returncode == 0:
            print_success("pip is available")
            return True
        else:
            print_error("pip is not available")
            return False
    except Exception:
        print_error("pip is not available")
        return False

def create_virtual_environment():
    """Create Python virtual environment"""
    venv_path = Path("venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists")
        return
    
    print_status("Creating Python virtual environment...")
    result = run_command([sys.executable, "-m", "venv", "venv"], check=False)
    if result.returncode == 0:
        print_success("Virtual environment created")
    else:
        print_error("Failed to create virtual environment")
        sys.exit(1)

def get_activation_command():
    """Get the command to activate virtual environment based on OS"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def get_python_executable():
    """Get Python executable path in virtual environment"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\python.exe"
    else:
        return "venv/bin/python"

def get_pip_executable():
    """Get pip executable path in virtual environment"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip.exe"
    else:
        return "venv/bin/pip"

def install_dependencies():
    """Install project dependencies"""
    print_status("Installing project dependencies...")
    
    # Upgrade pip first
    pip_exe = get_pip_executable()
    run_command([pip_exe, "install", "--upgrade", "pip"])
    
    # Install requirements
    if Path("requirements.txt").exists():
        run_command([pip_exe, "install", "-r", "requirements.txt"])
        print_success("Dependencies installed")
    else:
        print_error("requirements.txt not found")
        sys.exit(1)

def run_django_commands():
    """Run Django setup commands"""
    python_exe = get_python_executable()
    
    print_status("Running Django migrations...")
    run_command([python_exe, "manage.py", "makemigrations"])
    run_command([python_exe, "manage.py", "migrate"])
    print_success("Database migrations completed")

def create_superuser():
    """Create Django superuser"""
    print_status("Creating superuser account...")
    print_colored("Username: admin", Colors.YELLOW)
    print_colored("Email: admin@example.com", Colors.YELLOW)
    print_colored("Password: admin123", Colors.YELLOW)
    
    python_exe = get_python_executable()
    create_superuser_script = """
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully!')
else:
    print('Superuser already exists!')
"""
    run_command([python_exe, "-c", create_superuser_script])
    print_success("Superuser created")

def run_tests():
    """Run Django tests"""
    print_status("Running tests to verify installation...")
    python_exe = get_python_executable()
    result = run_command([python_exe, "manage.py", "test", "api"], check=False)
    if result.returncode == 0:
        print_success("All tests passed")
    else:
        print_error("Tests failed")
        sys.exit(1)

def create_sample_data():
    """Create sample data for the project"""
    print_status("Creating sample data...")
    
    python_exe = get_python_executable()
    sample_data_script = """
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
    {'title': 'Harry Potter and the Philosopher\\'s Stone', 'publication_year': 1997, 'author_name': 'J.K. Rowling', 'isbn': '9780747532699'},
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
"""
    run_command([python_exe, "-c", sample_data_script])
    print_success("Sample data created")

def print_final_instructions():
    """Print final setup instructions"""
    activation_cmd = get_activation_command()
    
    print_colored("\n" + "="*70, Colors.GREEN)
    print_colored("🎉 Setup completed successfully!", Colors.GREEN)
    print_colored("="*70, Colors.GREEN)
    
    print_colored("\n📋 Next steps:", Colors.BLUE)
    print_colored(f"1. Activate the virtual environment: {activation_cmd}", Colors.WHITE)
    print_colored("2. Start the development server: python manage.py runserver", Colors.WHITE)
    print_colored("3. Visit http://localhost:8000/api/ to see the API", Colors.WHITE)
    print_colored("4. Visit http://localhost:8000/admin/ to access Django admin", Colors.WHITE)
    print_colored("5. Use username 'admin' and password 'admin123' for admin access", Colors.WHITE)
    
    print_colored("\n🔧 Available API endpoints:", Colors.BLUE)
    print_colored("• GET  /api/                    - API root with navigation", Colors.WHITE)
    print_colored("• GET  /api/authors/            - List all authors", Colors.WHITE)
    print_colored("• GET  /api/books/               - List all books", Colors.WHITE)
    print_colored("• GET  /api/statistics/          - Get statistics", Colors.WHITE)
    print_colored("• GET  /api/authors/{id}/books/  - Get books by author", Colors.WHITE)
    
    print_colored("\n🧪 Run tests: python manage.py test api", Colors.BLUE)
    print_colored("📚 Read README.md for detailed documentation", Colors.BLUE)
    print_colored("\nHappy coding! 🚀", Colors.GREEN)

def main():
    """Main setup function"""
    print_colored("🚀 Setting up Advanced API Development with Django REST Framework", Colors.BLUE)
    print_colored("="*70, Colors.BLUE)
    
    # Check Python version
    check_python_version()
    
    # Check pip
    if not check_pip():
        sys.exit(1)
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install dependencies
    install_dependencies()
    
    # Run Django commands
    run_django_commands()
    
    # Create superuser
    create_superuser()
    
    # Run tests
    run_tests()
    
    # Create sample data
    create_sample_data()
    
    # Print final instructions
    print_final_instructions()

if __name__ == "__main__":
    main()