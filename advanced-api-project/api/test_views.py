from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from .models import Author, Book

User = get_user_model()


class AuthorModelTest(TestCase):
    """
    Test cases for the Author model.
    
    Tests model creation, validation, and string representation.
    """
    
    def setUp(self):
        """Set up test data for Author model tests."""
        self.author_data = {
            'name': 'Test Author'
        }
    
    def test_author_creation(self):
        """Test creating an author with valid data."""
        author = Author.objects.create(**self.author_data)
        self.assertEqual(author.name, 'Test Author')
        self.assertIsNotNone(author.created_at)
        self.assertIsNotNone(author.updated_at)
    
    def test_author_str_representation(self):
        """Test the string representation of an author."""
        author = Author.objects.create(**self.author_data)
        self.assertEqual(str(author), 'Test Author')
    
    def test_author_clean_method(self):
        """Test the clean method for author name formatting."""
        author = Author(name='  test author  ')
        author.clean()
        self.assertEqual(author.name, 'Test Author')


class BookModelTest(TestCase):
    """
    Test cases for the Book model.
    
    Tests model creation, validation, relationships, and string representation.
    """
    
    def setUp(self):
        """Set up test data for Book model tests."""
        self.author = Author.objects.create(name='Test Author')
        self.book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author,
            'isbn': '1234567890'
        }
    
    def test_book_creation(self):
        """Test creating a book with valid data."""
        book = Book.objects.create(**self.book_data)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2023)
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.isbn, '1234567890')
    
    def test_book_str_representation(self):
        """Test the string representation of a book."""
        book = Book.objects.create(**self.book_data)
        expected_str = 'Test Book by Test Author'
        self.assertEqual(str(book), expected_str)
    
    def test_book_clean_method_future_year(self):
        """Test validation for future publication year."""
        future_year = timezone.now().year + 1
        book = Book(
            title='Test Book',
            publication_year=future_year,
            author=self.author
        )
        with self.assertRaises(Exception):
            book.clean()
    
    def test_book_clean_method_isbn_formatting(self):
        """Test ISBN formatting in clean method."""
        book = Book(
            title='Test Book',
            publication_year=2023,
            author=self.author,
            isbn='123-456-789-0'
        )
        book.clean()
        self.assertEqual(book.isbn, '1234567890')


class AuthorAPITest(APITestCase):
    """
    Test cases for Author API endpoints.
    
    Tests CRUD operations, permissions, and response formats.
    """
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for Author API tests."""
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.author_data = {
            'name': 'Test Author'
        }
        cls.author = Author.objects.create(**cls.author_data)
    
    def setUp(self):
        """Set up for each test."""
        self.client = APIClient()
    
    def test_author_list_authenticated(self):
        """Test retrieving author list as authenticated user."""
        # Test with force_authenticate
        self.client.force_authenticate(user=self.user)
        url = reverse('api:author-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle pagination
        if 'results' in response.data:
            authors = response.data['results']
        else:
            authors = response.data
        self.assertIsInstance(authors, list)
        # Check that our test author is in the response
        author_names = [author['name'] for author in authors]
        self.assertIn('Test Author', author_names)
    
    def test_author_list_with_login(self):
        """Test retrieving author list using client.login authentication."""
        # Test with client.login method
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
        url = reverse('api:author-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle pagination
        if 'results' in response.data:
            authors = response.data['results']
        else:
            authors = response.data
        self.assertIsInstance(authors, list)
        
        # Logout after test
        self.client.logout()
    
    def test_author_list_unauthenticated(self):
        """Test retrieving author list as unauthenticated user."""
        url = reverse('api:author-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_author_create_authenticated(self):
        """Test creating an author as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:author-list-create')
        new_author_data = {'name': 'New Author'}
        response = self.client.post(url, new_author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
    
    def test_author_create_unauthenticated(self):
        """Test creating an author as unauthenticated user."""
        url = reverse('api:author-list-create')
        new_author_data = {'name': 'New Author'}
        response = self.client.post(url, new_author_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_author_detail_retrieve(self):
        """Test retrieving a specific author."""
        url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
    
    def test_author_update_authenticated(self):
        """Test updating an author as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
        update_data = {'name': 'Updated Author'}
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, 'Updated Author')
    
    def test_author_delete_authenticated(self):
        """Test deleting an author as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class BookAPITest(APITestCase):
    """
    Test cases for Book API endpoints.
    
    Tests CRUD operations, filtering, searching, and ordering.
    """
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for Book API tests."""
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.author = Author.objects.create(name='Test Author')
        cls.book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': cls.author,
            'isbn': '1234567890'
        }
        cls.book = Book.objects.create(**cls.book_data)
    
    def setUp(self):
        """Set up for each test."""
        self.client = APIClient()
    
    def test_book_list_authenticated(self):
        """Test retrieving book list as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle pagination
        if 'results' in response.data:
            books = response.data['results']
        else:
            books = response.data
        self.assertIsInstance(books, list)
        # Check that our test book is in the response
        book_titles = [book['title'] for book in books]
        self.assertIn('Test Book', book_titles)
    
    def test_book_list_with_login(self):
        """Test retrieving book list using client.login authentication."""
        # Test with client.login method
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
        url = reverse('api:book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle pagination
        if 'results' in response.data:
            books = response.data['results']
        else:
            books = response.data
        self.assertIsInstance(books, list)
        
        # Check that our test book is in the response
        book_titles = [book['title'] for book in books]
        self.assertIn('Test Book', book_titles)
        
        # Logout after test
        self.client.logout()
    
    def test_book_list_unauthenticated(self):
        """Test retrieving book list as unauthenticated user."""
        url = reverse('api:book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_create_authenticated(self):
        """Test creating a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-list-create')
        new_book_data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id,
            'isbn': '0987654321'
        }
        response = self.client.post(url, new_book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_book_create_unauthenticated(self):
        """Test creating a book as unauthenticated user."""
        url = reverse('api:book-list-create')
        new_book_data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(url, new_book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_create_future_year_validation(self):
        """Test creating a book with future publication year."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-list-create')
        future_year = timezone.now().year + 1
        invalid_book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        response = self.client.post(url, invalid_book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_book_search_functionality(self):
        """Test book search functionality."""
        url = reverse('api:book-list-create')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle pagination
        if 'results' in response.data:
            books = response.data['results']
        else:
            books = response.data
        self.assertIsInstance(books, list)
        # Check that our test book is in the search results
        book_titles = [book['title'] for book in books]
        self.assertIn('Test Book', book_titles)
    
    def test_book_ordering(self):
        """Test book ordering functionality."""
        # Create another book with different year
        Book.objects.create(
            title='Another Book',
            publication_year=2020,
            author=self.author
        )
        
        url = reverse('api:book-list-create')
        response = self.client.get(url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle pagination
        if 'results' in response.data:
            books = response.data['results']
        else:
            books = response.data
        self.assertIsInstance(books, list)
        # Check that we have at least 2 books
        self.assertGreaterEqual(len(books), 2)
        # Check that our test books are in the response
        book_titles = [book['title'] for book in books]
        self.assertIn('Test Book', book_titles)
        self.assertIn('Another Book', book_titles)
    
    def test_book_detail_retrieve(self):
        """Test retrieving a specific book."""
        url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_book_update_authenticated(self):
        """Test updating a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
        update_data = {
            'title': 'Updated Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_book_delete_authenticated(self):
        """Test deleting a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class AuthorBooksAPITest(APITestCase):
    """
    Test cases for the custom author-books endpoint.
    
    Tests retrieving books by author with search and ordering.
    """
    
    def setUp(self):
        """Set up test data for author-books API tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
        self.book1 = Book.objects.create(
            title='First Book',
            publication_year=2023,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Second Book',
            publication_year=2022,
            author=self.author
        )
    
    def test_author_books_retrieve(self):
        """Test retrieving books by author."""
        url = reverse('api:author-books', kwargs={'author_id': self.author.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 2)
        self.assertEqual(response.data['books_count'], 2)
    
    def test_author_books_search(self):
        """Test searching books by author with search parameter."""
        url = reverse('api:author-books', kwargs={'author_id': self.author.id})
        response = self.client.get(url, {'search': 'First'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'First Book')
    
    def test_author_books_ordering(self):
        """Test ordering books by author."""
        url = reverse('api:author-books', kwargs={'author_id': self.author.id})
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 2)
        # Should be ordered by title
        self.assertEqual(response.data['books'][0]['title'], 'First Book')
    
    def test_author_books_nonexistent_author(self):
        """Test retrieving books for non-existent author."""
        url = reverse('api:author-books', kwargs={'author_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookStatisticsAPITest(APITestCase):
    """
    Test cases for the book statistics endpoint.
    
    Tests retrieving aggregated statistics about books and authors.
    """
    
    def setUp(self):
        """Set up test data for statistics API tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        
        # Create books with different years
        Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author1
        )
        Book.objects.create(
            title='Book 2',
            publication_year=2023,
            author=self.author1
        )
        Book.objects.create(
            title='Book 3',
            publication_year=2021,
            author=self.author2
        )
    
    def test_book_statistics_retrieve(self):
        """Test retrieving book statistics."""
        url = reverse('api:book-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(data['total_books'], 3)
        self.assertEqual(data['total_authors'], 2)
        self.assertEqual(data['year_range']['earliest'], 2020)
        self.assertEqual(data['year_range']['latest'], 2023)
        self.assertEqual(len(data['books_per_year']), 3)
        self.assertEqual(len(data['top_authors']), 2)
    
    def test_book_statistics_empty_database(self):
        """Test statistics with empty database."""
        # Clear all data
        Book.objects.all().delete()
        Author.objects.all().delete()
        
        url = reverse('api:book-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(data['total_books'], 0)
        self.assertEqual(data['total_authors'], 0)
        self.assertIsNone(data['year_range']['earliest'])
        self.assertIsNone(data['year_range']['latest'])
        self.assertEqual(len(data['books_per_year']), 0)
        self.assertEqual(len(data['top_authors']), 0)


class APIRootTest(APITestCase):
    """
    Test cases for the API root endpoint.
    
    Tests the root endpoint that provides navigation links.
    """
    
    def test_api_root_retrieve(self):
        """Test retrieving the API root endpoint."""
        url = reverse('api:api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertIn('authors', data)
        self.assertIn('books', data)
        self.assertIn('filtering', data)
        self.assertIn('searching', data)
        self.assertIn('ordering', data)
        self.assertIn('authentication', data)