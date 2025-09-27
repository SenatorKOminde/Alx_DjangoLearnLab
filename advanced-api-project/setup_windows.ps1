# Advanced API Development with Django REST Framework - Windows PowerShell Setup Script
# This script sets up the project on Windows systems using PowerShell

param(
    [switch]$Force = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Cyan"
    White = "White"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Status {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" "Blue"
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "[SUCCESS] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" "Red"
}

# Check if running as administrator
if (([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "This script should not be run as administrator. Please run as a regular user."
    exit 1
}

Write-ColorOutput "`n🚀 Setting up Advanced API Development with Django REST Framework on Windows" "Blue"
Write-ColorOutput "==================================================================" "Blue"

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Success "Python is installed: $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-ColorOutput "Please install Python 3.8+ from https://python.org" "Yellow"
    Write-ColorOutput "Make sure to check 'Add Python to PATH' during installation" "Yellow"
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "pip not found"
    }
    Write-Success "pip is available: $pipVersion"
} catch {
    Write-Error "pip is not available"
    Write-ColorOutput "Please install pip or reinstall Python" "Yellow"
    exit 1
}

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath
Write-Status "Working directory: $(Get-Location)"

# Create virtual environment
Write-Status "Creating Python virtual environment..."
try {
    python -m venv venv
    Write-Success "Virtual environment created"
} catch {
    Write-Error "Failed to create virtual environment"
    exit 1
}

# Activate virtual environment
Write-Status "Activating virtual environment..."
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"
} catch {
    Write-Error "Failed to activate virtual environment"
    Write-ColorOutput "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" "Yellow"
    exit 1
}

# Upgrade pip
Write-Status "Upgrading pip..."
try {
    python -m pip install --upgrade pip
    Write-Success "pip upgraded"
} catch {
    Write-Error "Failed to upgrade pip"
    exit 1
}

# Install project dependencies
Write-Status "Installing project dependencies..."
try {
    pip install -r requirements.txt
    Write-Success "Dependencies installed"
} catch {
    Write-Error "Failed to install dependencies"
    exit 1
}

# Run Django migrations
Write-Status "Running Django migrations..."
try {
    python manage.py makemigrations
    python manage.py migrate
    Write-Success "Database migrations completed"
} catch {
    Write-Error "Failed to run migrations"
    exit 1
}

# Create superuser
Write-Status "Creating superuser account..."
Write-ColorOutput "Creating a superuser account for Django admin access..." "Yellow"
Write-ColorOutput "Username: admin" "Yellow"
Write-ColorOutput "Email: admin@example.com" "Yellow"
Write-ColorOutput "Password: admin123" "Yellow"

try {
    $createSuperuserScript = @"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully!')
else:
    print('Superuser already exists!')
"@
    python -c $createSuperuserScript
    Write-Success "Superuser created"
} catch {
    Write-Error "Failed to create superuser"
    exit 1
}

# Run tests
Write-Status "Running tests to verify installation..."
try {
    python manage.py test api
    Write-Success "All tests passed"
} catch {
    Write-Error "Tests failed"
    exit 1
}

# Create sample data
Write-Status "Creating sample data..."
try {
    $createSampleDataScript = @"
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
"@
    python -c $createSampleDataScript
    Write-Success "Sample data created"
} catch {
    Write-Error "Failed to create sample data"
    exit 1
}

Write-ColorOutput "`n==================================================================" "Green"
Write-ColorOutput "🎉 Setup completed successfully!" "Green"
Write-ColorOutput "==================================================================" "Green"

Write-ColorOutput "`n📋 Next steps:" "Blue"
Write-ColorOutput "1. Activate the virtual environment: .\venv\Scripts\Activate.ps1" "White"
Write-ColorOutput "2. Start the development server: python manage.py runserver" "White"
Write-ColorOutput "3. Visit http://localhost:8000/api/ to see the API" "White"
Write-ColorOutput "4. Visit http://localhost:8000/admin/ to access Django admin" "White"
Write-ColorOutput "5. Use username 'admin' and password 'admin123' for admin access" "White"

Write-ColorOutput "`n🔧 Available API endpoints:" "Blue"
Write-ColorOutput "• GET  /api/                    - API root with navigation" "White"
Write-ColorOutput "• GET  /api/authors/            - List all authors" "White"
Write-ColorOutput "• GET  /api/books/               - List all books" "White"
Write-ColorOutput "• GET  /api/statistics/          - Get statistics" "White"
Write-ColorOutput "• GET  /api/authors/{id}/books/  - Get books by author" "White"

Write-ColorOutput "`n🧪 Run tests: python manage.py test api" "Blue"
Write-ColorOutput "📚 Read README.md for detailed documentation" "Blue"
Write-ColorOutput "`nHappy coding! 🚀" "Green"