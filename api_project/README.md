# Django REST Framework API Project

This project demonstrates a simple API setup using Django and Django REST Framework (DRF).

## Features
- Book model with `title` and `author` fields
- API endpoints for listing and full CRUD operations on books
- Token-based authentication for secure access
- Permissions enforced for all API endpoints

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```

2. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

4. **API Endpoints:**
   - List books: `GET /api/books/`
   - CRUD operations: `GET/POST/PUT/DELETE /api/books_all/`
   - Obtain auth token: `POST /api/auth-token/` (with username & password)

## Authentication
- All API endpoints require authentication.
- Obtain a token via `/api/auth-token/` and include it in the `Authorization` header as `Token <your_token>`.

## Permissions
- Only authenticated users can access API endpoints.
- Permissions are set in `settings.py` and enforced in views.

## Project Structure
```
api_project/
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── api_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
└── README.md
```

## License
MIT
