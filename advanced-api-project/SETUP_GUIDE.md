# Setup Guide - Advanced API Development with Django REST Framework

This guide provides multiple ways to set up the Advanced API Development project on different operating systems.

## 🚀 Quick Setup Options

### Option 1: Cross-Platform Python Script (Recommended)
Works on Windows, macOS, and Linux:

```bash
python setup.py
```

### Option 2: Ubuntu/Debian
```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### Option 3: Windows Command Prompt
```cmd
setup_windows.bat
```

### Option 4: Windows PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_windows.ps1
```

## 📋 Prerequisites

### All Platforms
- **Python 3.8+** - Download from [python.org](https://python.org)
- **pip** - Usually comes with Python
- **Git** - For version control (optional)

### Ubuntu/Debian Additional Requirements
- `build-essential` - For compiling Python packages
- `python3-dev` - Python development headers
- `libssl-dev`, `libffi-dev` - SSL and FFI libraries

## 🔧 Manual Setup (If Scripts Don't Work)

### 1. Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd advanced-api-project

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run Django Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Create Sample Data (Optional)
```bash
python manage.py shell
```

Then run this Python code:
```python
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
    Author.objects.get_or_create(name=author_data['name'])

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
    Book.objects.get_or_create(
        title=book_data['title'],
        author=author,
        defaults={
            'publication_year': book_data['publication_year'],
            'isbn': book_data['isbn']
        }
    )
```

### 6. Run Tests
```bash
python manage.py test api
```

### 7. Start Development Server
```bash
python manage.py runserver
```

## 🎯 What the Setup Scripts Do

### Automatic Setup Process:
1. **Check Prerequisites** - Verify Python and pip are installed
2. **Create Virtual Environment** - Isolated Python environment
3. **Install Dependencies** - All required packages from requirements.txt
4. **Run Database Migrations** - Set up the database schema
5. **Create Superuser** - Admin account for Django admin
6. **Run Tests** - Verify everything works correctly
7. **Create Sample Data** - Populate with example books and authors

### Default Credentials:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `admin123`

## 🌐 Access Points After Setup

### API Endpoints:
- **API Root**: http://localhost:8000/api/
- **Authors**: http://localhost:8000/api/authors/
- **Books**: http://localhost:8000/api/books/
- **Statistics**: http://localhost:8000/api/statistics/

### Admin Interface:
- **Django Admin**: http://localhost:8000/admin/
- **Login**: Use the credentials created during setup

## 🐛 Troubleshooting

### Common Issues:

#### 1. Python Not Found
```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not installed, download from python.org
```

#### 2. Permission Denied (Ubuntu)
```bash
# Make scripts executable
chmod +x setup_ubuntu.sh
chmod +x setup.py
```

#### 3. PowerShell Execution Policy (Windows)
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Virtual Environment Issues
```bash
# Remove existing venv and recreate
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
python -m venv venv
```

#### 5. Database Issues
```bash
# Reset database
rm db.sqlite3  # Linux/macOS
del db.sqlite3  # Windows
python manage.py migrate
```

#### 6. Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Getting Help:

1. **Check the logs** - Look for error messages in the terminal
2. **Verify Python version** - Must be 3.8 or higher
3. **Check virtual environment** - Make sure it's activated
4. **Run tests** - `python manage.py test api` to verify setup
5. **Read the README** - Check README.md for detailed documentation

## 📚 Next Steps

After successful setup:

1. **Explore the API** - Visit http://localhost:8000/api/
2. **Read the Documentation** - Check README.md for API usage
3. **Run Tests** - `python manage.py test api` to verify functionality
4. **Customize** - Modify models, views, or serializers as needed
5. **Deploy** - Follow Django deployment guides for production

## 🎉 Success Indicators

You'll know the setup was successful when:
- ✅ All tests pass (`python manage.py test api`)
- ✅ Server starts without errors (`python manage.py runserver`)
- ✅ API endpoints respond correctly
- ✅ Django admin is accessible
- ✅ Sample data is visible in the API

Happy coding! 🚀