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
    
    # Author specific views
    path('authors/list/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # Book endpoints
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Book specific views
    path('books/list/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookListCreateView.as_view(), name='book-create'),
    path('books/update/', views.BookUpdateView.as_view(), name='book-update-generic'),
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete-generic'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Generic views with exact naming patterns
    path('generic/list/', views.ListView.as_view(), name='generic-list'),
    path('generic/<int:pk>/update/', views.UpdateView.as_view(), name='generic-update'),
    path('generic/<int:pk>/delete/', views.DeleteView.as_view(), name='generic-delete'),
    
    # Statistics endpoint
    path('statistics/', views.book_statistics, name='book-statistics'),
]