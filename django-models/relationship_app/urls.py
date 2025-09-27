from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view URLs
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('books-list/', views.BookListView.as_view(), name='book_list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]