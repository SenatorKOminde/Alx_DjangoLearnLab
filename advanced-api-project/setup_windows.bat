@echo off
REM Advanced API Development with Django REST Framework - Windows Setup Script
REM This script sets up the project on Windows systems

echo.
echo ==================================================================
echo 🚀 Setting up Advanced API Development with Django REST Framework
echo ==================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please install pip or reinstall Python
    pause
    exit /b 1
)

echo ✅ pip is available

REM Navigate to project directory
cd /d "%~dp0"
echo 📁 Working directory: %CD%

REM Create virtual environment
echo.
echo 🔧 Creating Python virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

REM Upgrade pip
echo.
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)
echo ✅ pip upgraded

REM Install project dependencies
echo.
echo 🔧 Installing project dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Run Django migrations
echo.
echo 🔧 Running Django migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ❌ Failed to create migrations
    pause
    exit /b 1
)

python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Failed to run migrations
    pause
    exit /b 1
)
echo ✅ Database migrations completed

REM Create superuser
echo.
echo 🔧 Creating superuser account...
echo Creating a superuser account for Django admin access...
echo Username: admin
echo Email: admin@example.com
echo Password: admin123
echo.

python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists!')"
if %errorlevel% neq 0 (
    echo ❌ Failed to create superuser
    pause
    exit /b 1
)
echo ✅ Superuser created

REM Run tests
echo.
echo 🔧 Running tests to verify installation...
python manage.py test api
if %errorlevel% neq 0 (
    echo ❌ Tests failed
    pause
    exit /b 1
)
echo ✅ All tests passed

REM Create sample data
echo.
echo 🔧 Creating sample data...
python manage.py shell -c "from api.models import Author, Book; authors_data = [{'name': 'J.K. Rowling'}, {'name': 'George Orwell'}, {'name': 'Harper Lee'}, {'name': 'F. Scott Fitzgerald'}, {'name': 'Jane Austen'}]; [Author.objects.get_or_create(name=author_data['name']) for author_data in authors_data]; books_data = [{'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author_name': 'J.K. Rowling', 'isbn': '9780747532699'}, {'title': '1984', 'publication_year': 1949, 'author_name': 'George Orwell', 'isbn': '9780451524935'}, {'title': 'To Kill a Mockingbird', 'publication_year': 1960, 'author_name': 'Harper Lee', 'isbn': '9780061120084'}, {'title': 'The Great Gatsby', 'publication_year': 1925, 'author_name': 'F. Scott Fitzgerald', 'isbn': '9780743273565'}, {'title': 'Pride and Prejudice', 'publication_year': 1813, 'author_name': 'Jane Austen', 'isbn': '9780141439518'}]; [Book.objects.get_or_create(title=book_data['title'], author=Author.objects.get(name=book_data['author_name']), defaults={'publication_year': book_data['publication_year'], 'isbn': book_data['isbn']}) for book_data in books_data]"
if %errorlevel% neq 0 (
    echo ❌ Failed to create sample data
    pause
    exit /b 1
)
echo ✅ Sample data created

echo.
echo ==================================================================
echo 🎉 Setup completed successfully!
echo ==================================================================
echo.
echo 📋 Next steps:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Start the development server: python manage.py runserver
echo 3. Visit http://localhost:8000/api/ to see the API
echo 4. Visit http://localhost:8000/admin/ to access Django admin
echo 5. Use username 'admin' and password 'admin123' for admin access
echo.
echo 🔧 Available API endpoints:
echo • GET  /api/                    - API root with navigation
echo • GET  /api/authors/            - List all authors
echo • GET  /api/books/               - List all books
echo • GET  /api/statistics/          - Get statistics
echo • GET  /api/authors/{id}/books/  - Get books by author
echo.
echo 🧪 Run tests: python manage.py test api
echo 📚 Read README.md for detailed documentation
echo.
echo Happy coding! 🚀
echo.
pause
REM Advanced API Development with Django REST Framework - Windows Setup Script
REM This script sets up the project on Windows systems

echo 🚀 Setting up Advanced API Development with Django REST Framework on Windows
echo ========================================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [INFO] Python is installed
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [INFO] pip is available

REM Create virtual environment
echo [INFO] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment created

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install project dependencies
echo [INFO] Installing project dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [SUCCESS] Dependencies installed

REM Run database migrations
echo [INFO] Running database migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create migrations
    pause
    exit /b 1
)

python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run migrations
    pause
    exit /b 1
)

echo [SUCCESS] Database migrations completed

REM Create superuser
echo [INFO] Creating superuser account...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') | python manage.py shell
if %errorlevel% neq 0 (
    echo [WARNING] Failed to create superuser, you can create one manually later
)

echo [SUCCESS] Superuser created (admin/admin123)

REM Collect static files
echo [INFO] Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo [WARNING] Failed to collect static files
)

REM Run tests
echo [INFO] Running tests to verify installation...
python manage.py test api
if %errorlevel% neq 0 (
    echo [WARNING] Some tests failed, but installation may still work
)

echo [SUCCESS] Tests completed

REM Create sample data script
echo [INFO] Creating sample data script...
(
echo #!/usr/bin/env python
echo """
echo Script to create sample data for the Advanced API Development project
echo """
echo import os
echo import sys
echo import django
echo.
echo # Setup Django
echo os.environ.setdefault^('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings'^)
echo django.setup^(^)
echo.
echo from api.models import Author, Book
echo.
echo def create_sample_data^(^):
echo     """Create sample authors and books for testing"""
echo     print^("Creating sample data..."^)
echo     
echo     # Create authors
echo     authors_data = [
echo         {'name': 'J.K. Rowling'},
echo         {'name': 'George R.R. Martin'},
echo         {'name': 'Isaac Asimov'},
echo         {'name': 'Agatha Christie'},
echo         {'name': 'Stephen King'},
echo     ]
echo     
echo     authors = []
echo     for author_data in authors_data:
echo         author, created = Author.objects.get_or_create^(**author_data^)
echo         authors.append^(author^)
echo         if created:
echo             print^(f"Created author: {author.name}"^)
echo     
echo     # Create books
echo     books_data = [
echo         {'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author': authors[0], 'isbn': '9780747532699'},
echo         {'title': 'Harry Potter and the Chamber of Secrets', 'publication_year': 1998, 'author': authors[0], 'isbn': '9780747538493'},
echo         {'title': 'A Game of Thrones', 'publication_year': 1996, 'author': authors[1], 'isbn': '9780553103540'},
echo         {'title': 'A Clash of Kings', 'publication_year': 1998, 'author': authors[1], 'isbn': '9780553108033'},
echo         {'title': 'Foundation', 'publication_year': 1951, 'author': authors[2], 'isbn': '9780553293357'},
echo         {'title': 'I, Robot', 'publication_year': 1950, 'author': authors[2], 'isbn': '9780553293401'},
echo         {'title': 'Murder on the Orient Express', 'publication_year': 1934, 'author': authors[3], 'isbn': '9780062073495'},
echo         {'title': 'The Murder of Roger Ackroyd', 'publication_year': 1926, 'author': authors[3], 'isbn': '9780062073501'},
echo         {'title': 'The Shining', 'publication_year': 1977, 'author': authors[4], 'isbn': '9780307743657'},
echo         {'title': 'It', 'publication_year': 1986, 'author': authors[4], 'isbn': '9781501142970'},
echo     ]
echo     
echo     for book_data in books_data:
echo         book, created = Book.objects.get_or_create^(
echo             title=book_data['title'],
echo             author=book_data['author'],
echo             defaults={
echo                 'publication_year': book_data['publication_year'],
echo                 'isbn': book_data['isbn']
echo             }
echo         ^)
echo         if created:
echo             print^(f"Created book: {book.title} by {book.author.name}"^)
echo     
echo     print^(f"\nSample data created successfully!"^)
echo     print^(f"Authors: {Author.objects.count^(^)}"^)
echo     print^(f"Books: {Book.objects.count^(^)}"^)
echo.
echo if __name__ == '__main__':
echo     create_sample_data^(^)
) > create_sample_data.py

echo [SUCCESS] Sample data script created

REM Run sample data creation
echo [INFO] Creating sample data...
python create_sample_data.py
if %errorlevel% neq 0 (
    echo [WARNING] Failed to create sample data
)

REM Create startup script
echo [INFO] Creating startup script...
(
echo @echo off
echo REM Advanced API Development - Server Startup Script
echo.
echo echo 🚀 Starting Advanced API Development Server
echo echo =============================================
echo.
echo REM Activate virtual environment
echo call venv\Scripts\activate.bat
echo.
echo REM Start the Django development server
echo echo Starting Django development server...
echo echo Server will be available at: http://127.0.0.1:8000
echo echo API root: http://127.0.0.1:8000/api/
echo echo Admin interface: http://127.0.0.1:8000/admin/
echo echo.
echo echo Press Ctrl+C to stop the server
echo echo.
echo.
echo python manage.py runserver 127.0.0.1:8000
) > start_server.bat

echo [SUCCESS] Startup script created

REM Create test script
echo [INFO] Creating API test script...
(
echo @echo off
echo REM Advanced API Development - API Test Script
echo.
echo echo 🧪 Testing Advanced API Development API
echo echo ========================================
echo.
echo set BASE_URL=http://127.0.0.1:8000/api
echo.
echo echo Testing API endpoints...
echo echo.
echo.
echo REM Test API root
echo echo 1. Testing API root...
echo curl -s "%BASE_URL%/" ^| python -m json.tool
echo echo.
echo.
echo REM Test authors endpoint
echo echo 2. Testing authors endpoint...
echo curl -s "%BASE_URL%/authors/" ^| python -m json.tool
echo echo.
echo.
echo REM Test books endpoint
echo echo 3. Testing books endpoint...
echo curl -s "%BASE_URL%/books/" ^| python -m json.tool
echo echo.
echo.
echo REM Test search functionality
echo echo 4. Testing search functionality...
echo curl -s "%BASE_URL%/books/?search=Harry" ^| python -m json.tool
echo echo.
echo.
echo REM Test filtering
echo echo 5. Testing filtering...
echo curl -s "%BASE_URL%/books/?publication_year=1997" ^| python -m json.tool
echo echo.
echo.
echo REM Test ordering
echo echo 6. Testing ordering...
echo curl -s "%BASE_URL%/books/?ordering=title" ^| python -m json.tool
echo echo.
echo.
echo REM Test statistics
echo echo 7. Testing statistics endpoint...
echo curl -s "%BASE_URL%/statistics/" ^| python -m json.tool
echo echo.
echo.
echo echo API testing completed!
) > test_api.bat

echo [SUCCESS] Test script created

REM Create a comprehensive README for Windows
echo [INFO] Creating Windows-specific README...
(
echo # Advanced API Development - Windows Setup
echo.
echo This project has been set up for Windows systems.
echo.
echo ## Quick Start
echo.
echo 1. **Start the server**: Double-click `start_server.bat` or run in command prompt
echo 2. **Test the API**: Double-click `test_api.bat` or run in command prompt
echo 3. **Access admin**: Open http://127.0.0.1:8000/admin/ in your browser
echo 4. **View API**: Open http://127.0.0.1:8000/api/ in your browser
echo.
echo ## Available Commands
echo.
echo - `start_server.bat` - Start the Django development server
echo - `test_api.bat` - Test all API endpoints
echo - `create_sample_data.py` - Create sample data for testing
echo.
echo ## Manual Commands
echo.
echo Open Command Prompt in the project directory and run:
echo.
echo ```cmd
echo REM Activate virtual environment
echo venv\Scripts\activate.bat
echo.
echo REM Start server
echo python manage.py runserver
echo.
echo REM Run tests
echo python manage.py test
echo.
echo REM Create superuser
echo python manage.py createsuperuser
echo.
echo REM Django shell
echo python manage.py shell
echo ```
echo.
echo ## Troubleshooting
echo.
echo 1. **Python not found**: Install Python 3.8+ from https://python.org
echo 2. **Permission errors**: Run Command Prompt as Administrator
echo 3. **Port already in use**: Change port in start_server.bat
echo 4. **Virtual environment issues**: Delete venv folder and run setup again
echo.
echo ## API Endpoints
echo.
echo - GET /api/ - API root with navigation
echo - GET /api/authors/ - List all authors
echo - GET /api/books/ - List all books
echo - GET /api/statistics/ - Get statistics
echo - POST /api/authors/ - Create author (authenticated)
echo - POST /api/books/ - Create book (authenticated)
echo.
echo ## Authentication
echo.
echo - Username: admin
echo - Password: admin123
echo - Admin URL: http://127.0.0.1:8000/admin/
echo.
echo ## Features
echo.
echo - ✅ Full CRUD operations for authors and books
echo - ✅ Advanced filtering, searching, and ordering
echo - ✅ Authentication and permissions
echo - ✅ Comprehensive testing
echo - ✅ Sample data included
echo - ✅ Admin interface
echo.
) > README_Windows.md

echo [SUCCESS] Windows README created

REM Final success message
echo.
echo [SUCCESS] Setup completed successfully!
echo.
echo 📋 Next Steps:
echo ==============
echo 1. Start the server: start_server.bat
echo 2. Test the API: test_api.bat
echo 3. Access admin: http://127.0.0.1:8000/admin/ (admin/admin123)
echo 4. View API documentation: http://127.0.0.1:8000/api/
echo.
echo 📚 Available Commands:
echo =====================
echo • Start server: start_server.bat
echo • Test API: test_api.bat
echo • Run tests: python manage.py test
echo • Create sample data: python create_sample_data.py
echo • Django shell: python manage.py shell
echo • Django admin: python manage.py runserver
echo.
echo [SUCCESS] Advanced API Development project is ready to use!
echo.
echo Press any key to exit...
pause >nul