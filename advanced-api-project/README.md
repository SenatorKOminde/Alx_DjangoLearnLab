# Advanced API Development with Django REST Framework

This project demonstrates advanced API development concepts using Django REST Framework, including custom serializers, generic views, filtering, searching, ordering, and comprehensive testing.

## Project Overview

The Advanced API Project is a Django REST Framework application that manages a library of books and authors. It showcases advanced API development techniques including:

- Custom serializers with nested relationships
- Generic views for CRUD operations
- Advanced filtering, searching, and ordering
- Authentication and permissions
- Comprehensive unit testing
- Custom API endpoints for statistics

## Features

### Models
- **Author Model**: Stores author information with name, timestamps
- **Book Model**: Stores book information with title, publication year, author relationship, ISBN

### API Endpoints

#### Authors
- `GET /api/authors/` - List all authors
- `POST /api/authors/` - Create new author (authenticated)
- `GET /api/authors/{id}/` - Get specific author details
- `PUT/PATCH /api/authors/{id}/` - Update author (authenticated)
- `DELETE /api/authors/{id}/` - Delete author (authenticated)
- `GET /api/authors/{id}/books/` - Get books by specific author

#### Books
- `GET /api/books/` - List all books with filtering, searching, ordering
- `POST /api/books/` - Create new book (authenticated)
- `GET /api/books/{id}/` - Get specific book details
- `PUT/PATCH /api/books/{id}/` - Update book (authenticated)
- `DELETE /api/books/{id}/` - Delete book (authenticated)

#### Statistics
- `GET /api/statistics/` - Get aggregated statistics about books and authors

#### Root
- `GET /api/` - API root with navigation links

### Advanced Features

#### Filtering
Books can be filtered by:
- Title (partial match)
- Author name (partial match)
- Publication year
- ISBN (partial match)

#### Searching
Books can be searched across:
- Title
- Author name
- ISBN

#### Ordering
Books can be ordered by:
- Title (ascending/descending)
- Publication year (ascending/descending)
- Creation date (ascending/descending)
- Update date (ascending/descending)

#### Pagination
All list endpoints support pagination with 20 items per page.

## 🚀 Quick Setup

### Automated Setup (Recommended)

#### Cross-Platform Setup
```bash
# Run the universal setup script
python setup.py
```

#### Ubuntu/Linux Setup
```bash
# Make executable and run
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

#### Windows Command Prompt
```cmd
# Run the Windows setup script
setup_windows.bat
```

#### Windows PowerShell
```powershell
# Set execution policy and run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_windows.ps1
```

### 🔧 What the Setup Scripts Do

The automated setup scripts will:
- ✅ Check Python and pip installation
- ✅ Create isolated virtual environment
- ✅ Install all required dependencies
- ✅ Run database migrations
- ✅ Create admin superuser (admin/admin123)
- ✅ Run comprehensive tests
- ✅ Create sample data (books and authors)
- ✅ Provide detailed setup instructions

### 📚 Detailed Setup Guide

For troubleshooting and detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

### Manual Setup

#### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd advanced-api-project
   ```

2. **Create and activate virtual environment**
   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Create sample data**
   ```bash
   python create_sample_data.py
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### 🎯 Quick Start Scripts

After setup, use these scripts:

#### Ubuntu/Linux
```bash
./start_server.sh    # Start the server
./test_api.sh        # Test the API
```

#### Windows
```cmd
start_server.bat     # Start the server
test_api.bat         # Test the API
```

## API Usage Examples

### Authentication
The API uses Django's built-in authentication system. For testing, you can:
1. Use the Django admin interface at `/admin/`
2. Use Basic Authentication with username/password
3. Use Session Authentication (login via admin)

### Example API Calls

#### Get all books
```bash
curl -X GET http://localhost:8000/api/books/
```

#### Search books
```bash
curl -X GET "http://localhost:8000/api/books/?search=python"
```

#### Filter books by year
```bash
curl -X GET "http://localhost:8000/api/books/?publication_year=2023"
```

#### Order books by title
```bash
curl -X GET "http://localhost:8000/api/books/?ordering=title"
```

#### Create a new book (authenticated)
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "Advanced Python Programming",
    "publication_year": 2023,
    "author": 1,
    "isbn": "9781234567890"
  }'
```

#### Get author with books
```bash
curl -X GET http://localhost:8000/api/authors/1/
```

#### Get books by author
```bash
curl -X GET http://localhost:8000/api/authors/1/books/
```

#### Get statistics
```bash
curl -X GET http://localhost:8000/api/statistics/
```

## Testing

The project includes comprehensive unit tests covering:
- Model validation and relationships
- API endpoint functionality
- Authentication and permissions
- Filtering, searching, and ordering
- Custom endpoints

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test api

# Run with verbose output
python manage.py test api -v 2
```

### Test Coverage
The test suite includes:
- **Model Tests**: Validation, relationships, string representations
- **API Tests**: CRUD operations, permissions, response formats
- **Filtering Tests**: Search functionality, ordering, filtering
- **Custom Endpoint Tests**: Statistics, author-books relationships
- **Authentication Tests**: Permission enforcement, access control

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py          # Django settings with DRF configuration
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── models.py           # Author and Book models
│   ├── serializers.py      # Custom serializers with validation
│   ├── views.py            # API views and custom endpoints
│   ├── urls.py             # API URL patterns
│   └── test_views.py       # Comprehensive unit tests
├── manage.py
├── requirements.txt
└── README.md
```

## Key Implementation Details

### Custom Serializers
- **BookSerializer**: Handles book serialization with custom validation
- **AuthorSerializer**: Includes nested book relationships
- **List Serializers**: Optimized for list views with reduced data

### Generic Views
- **ListCreateAPIView**: For listing and creating resources
- **RetrieveUpdateDestroyAPIView**: For detailed operations
- **Custom mixins**: For specialized functionality

### Filtering and Search
- **DjangoFilterBackend**: For field-based filtering
- **SearchFilter**: For text-based searching
- **OrderingFilter**: For result ordering

### Authentication and Permissions
- **SessionAuthentication**: For web interface
- **BasicAuthentication**: For API clients
- **IsAuthenticatedOrReadOnly**: Read access for all, write for authenticated users

### Custom Endpoints
- **Author Books**: Get all books by a specific author
- **Statistics**: Aggregated data about books and authors
- **API Root**: Navigation hub for the API

## Advanced Features Demonstrated

1. **Custom Validation**: Publication year validation, ISBN formatting
2. **Nested Relationships**: Author serializer includes related books
3. **Optimized Queries**: Using select_related and prefetch_related
4. **Custom Permissions**: Different access levels for different operations
5. **Pagination**: Built-in pagination for large datasets
6. **Error Handling**: Comprehensive error responses and validation
7. **Documentation**: Extensive inline documentation and comments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is part of the ALX Django Learning Lab curriculum and is for educational purposes.

## Contact

For questions or issues, please refer to the ALX Django Learning Lab documentation or create an issue in the repository.