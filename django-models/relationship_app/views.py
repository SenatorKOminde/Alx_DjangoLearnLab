from .models import Library
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Book, Library, Author

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Renders a simple text list of book titles and their authors.
    """
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all books in this library
        context['books'] = self.object.books.select_related('author').all()
        return context

# Additional views for better functionality
class BookListView(ListView):
    """
    Class-based view to list all books with pagination.
    """
    model = Book
    template_name = 'relationship_app/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    
    def get_queryset(self):
        return Book.objects.select_related('author').all()

class AuthorDetailView(DetailView):
    """
    Class-based view to display author details and their books.
    """
    model = Author
    template_name = 'relationship_app/author_detail.html'
    context_object_name = 'author'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all books by this author
        context['books'] = self.object.books.all()
        return context

# Authentication Views
class CustomLoginView(LoginView):
    """
    Custom login view using Django's built-in LoginView.
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('relationship_app:list_books')

class CustomLogoutView(LogoutView):
    """
    Custom logout view using Django's built-in LogoutView.
    """
    template_name = 'relationship_app/logout.html'
    next_page = reverse_lazy('relationship_app:list_books')

def register_view(request):
    """
    Function-based view for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    View to display user profile (requires login).
    """
    return render(request, 'relationship_app/profile.html', {'user': request.user})
