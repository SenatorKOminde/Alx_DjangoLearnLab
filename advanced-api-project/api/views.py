from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.db.models import Q, Min, Max, Count
from .models import Author, Book
from .serializers import (
    AuthorSerializer, AuthorListSerializer,
    BookSerializer, BookListSerializer
)


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    View for listing all authors and creating new authors.
    
    GET: Returns a list of all authors with their book counts.
    POST: Creates a new author with the provided data.
    """
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """
        Return different serializers for list and create operations.
        """
        if self.request.method == 'GET':
            return AuthorListSerializer
        return AuthorSerializer

    def get_queryset(self):
        """
        Return queryset with optimized queries for list view.
        """
        return Author.objects.prefetch_related('books').all()


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific author.
    
    GET: Returns detailed information about a specific author including their books.
    PUT/PATCH: Updates an existing author.
    DELETE: Deletes an author (and all their books due to CASCADE).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return queryset with optimized queries for detail view.
        """
        return Author.objects.prefetch_related('books').all()


class BookListCreateView(generics.ListCreateAPIView):
    """
    View for listing all books and creating new books.
    
    GET: Returns a list of all books with filtering, searching, and ordering.
    POST: Creates a new book with the provided data.
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'isbn']
    ordering_fields = ['title', 'publication_year', 'created_at', 'updated_at']
    ordering = ['-publication_year', 'title']

    def get_serializer_class(self):
        """
        Return different serializers for list and create operations.
        """
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer

    def get_queryset(self):
        """
        Return queryset with optimized queries for list view.
        """
        return Book.objects.select_related('author').all()

    def perform_create(self, serializer):
        """
        Customize the creation process for books.
        """
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific book.
    
    GET: Returns detailed information about a specific book.
    PUT/PATCH: Updates an existing book.
    DELETE: Deletes a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return queryset with optimized queries for detail view.
        """
        return Book.objects.select_related('author').all()


# Additional specific views for more granular control

class AuthorListView(generics.ListAPIView):
    """
    Dedicated view for listing all authors.
    
    GET: Returns a list of all authors with their book counts.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Return queryset with optimized queries for list view.
        """
        return Author.objects.prefetch_related('books').all()


class AuthorUpdateView(generics.UpdateAPIView):
    """
    Dedicated view for updating an author.
    
    PUT/PATCH: Updates an existing author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return queryset with optimized queries for update view.
        """
        return Author.objects.all()


class AuthorDeleteView(generics.DestroyAPIView):
    """
    Dedicated view for deleting an author.
    
    DELETE: Deletes an author (and all their books due to CASCADE).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return queryset with optimized queries for delete view.
        """
        return Author.objects.all()


class BookListView(generics.ListAPIView):
    """
    Dedicated view for listing all books with filtering, searching, and ordering.
    
    GET: Returns a list of all books with advanced query capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'isbn']
    ordering_fields = ['title', 'publication_year', 'created_at', 'updated_at']
    ordering = ['-publication_year', 'title']

    def get_queryset(self):
        """
        Return queryset with optimized queries for list view.
        """
        return Book.objects.select_related('author').all()


class BookUpdateView(generics.UpdateAPIView):
    """
    Dedicated view for updating a book.
    
    PUT/PATCH: Updates an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return queryset with optimized queries for update view.
        """
        return Book.objects.select_related('author').all()


class BookDeleteView(generics.DestroyAPIView):
    """
    Dedicated view for deleting a book.
    
    DELETE: Deletes a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return queryset with optimized queries for delete view.
        """
        return Book.objects.select_related('author').all()


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_root(request):
    """
    Root endpoint that provides links to all available API endpoints.
    
    This endpoint serves as a navigation hub for the API, providing
    clear links to all available resources and their operations.
    """
    return Response({
        'authors': {
            'list': request.build_absolute_uri('/api/authors/'),
            'create': request.build_absolute_uri('/api/authors/'),
            'list_only': request.build_absolute_uri('/api/authors/list/'),
            'update': request.build_absolute_uri('/api/authors/{id}/update/'),
            'delete': request.build_absolute_uri('/api/authors/{id}/delete/'),
        },
        'books': {
            'list': request.build_absolute_uri('/api/books/'),
            'create': request.build_absolute_uri('/api/books/'),
            'list_only': request.build_absolute_uri('/api/books/list/'),
            'update': request.build_absolute_uri('/api/books/{id}/update/'),
            'delete': request.build_absolute_uri('/api/books/{id}/delete/'),
        },
        'filtering': {
            'books_by_title': request.build_absolute_uri('/api/books/?title=search_term'),
            'books_by_author': request.build_absolute_uri('/api/books/?author_name=author_name'),
            'books_by_year': request.build_absolute_uri('/api/books/?publication_year=2023'),
            'books_by_year_range': request.build_absolute_uri('/api/books/?publication_year_min=2020&publication_year_max=2023'),
        },
        'searching': {
            'books_search': request.build_absolute_uri('/api/books/?search=search_term'),
        },
        'ordering': {
            'books_by_title': request.build_absolute_uri('/api/books/?ordering=title'),
            'books_by_year': request.build_absolute_uri('/api/books/?ordering=-publication_year'),
        },
        'authentication': {
            'login': request.build_absolute_uri('/admin/login/'),
            'logout': request.build_absolute_uri('/admin/logout/'),
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def author_books(request, author_id):
    """
    Custom endpoint to get all books by a specific author.
    
    This endpoint provides a specialized view for retrieving all books
    written by a particular author with optimized queries.
    """
    try:
        author = Author.objects.prefetch_related('books').get(id=author_id)
        books = author.books.all()
        
        # Apply search and ordering if provided
        search = request.GET.get('search', '')
        if search:
            books = books.filter(
                Q(title__icontains=search) | 
                Q(isbn__icontains=search)
            )
        
        ordering = request.GET.get('ordering', '-publication_year')
        if ordering:
            books = books.order_by(ordering)
        
        serializer = BookListSerializer(books, many=True)
        
        return Response({
            'author': AuthorListSerializer(author).data,
            'books': serializer.data,
            'books_count': books.count()
        })
        
    except Author.DoesNotExist:
        return Response(
            {'error': 'Author not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def book_statistics(request):
    """
    Custom endpoint to get statistics about books and authors.
    
    This endpoint provides aggregated statistics about the book collection
    including total counts, year ranges, and author statistics.
    """
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    
    if total_books > 0:
        earliest_year = Book.objects.aggregate(
            earliest=Min('publication_year')
        )['earliest']
        latest_year = Book.objects.aggregate(
            latest=Max('publication_year')
        )['latest']
        
        # Get books per year
        books_per_year = Book.objects.values('publication_year').annotate(
            count=Count('id')
        ).order_by('publication_year')
        
        # Get authors with most books
        top_authors = Author.objects.annotate(
            book_count=Count('books')
        ).order_by('-book_count')[:5]
    else:
        earliest_year = None
        latest_year = None
        books_per_year = []
        top_authors = []
    
    return Response({
        'total_books': total_books,
        'total_authors': total_authors,
        'year_range': {
            'earliest': earliest_year,
            'latest': latest_year
        },
        'books_per_year': list(books_per_year),
        'top_authors': AuthorListSerializer(top_authors, many=True).data
    })