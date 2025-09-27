from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Root API endpoint
    path('', views.api_root, name='api-root'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:author_id>/books/', views.author_books, name='author-books'),
    
    # Book endpoints
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Statistics endpoint
    path('statistics/', views.book_statistics, name='book-statistics'),
]