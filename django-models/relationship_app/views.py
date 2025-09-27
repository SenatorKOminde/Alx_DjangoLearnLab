from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.forms import ModelForm
from .models import Book, Library, Author, UserProfile

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

# Role-based access control functions
def is_admin(user):
    """Check if user has Admin role."""
    try:
        return user.userprofile.role == 'Admin'
    except:
        return False

def is_librarian(user):
    """Check if user has Librarian role."""
    try:
        return user.userprofile.role == 'Librarian'
    except:
        return False

def is_member(user):
    """Check if user has Member role."""
    try:
        return user.userprofile.role == 'Member'
    except:
        return False

# Role-based views
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin view that only users with Admin role can access.
    """
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian view accessible only to users with Librarian role.
    """
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

@login_required
@user_passes_test(is_member)
def member_view(request):
    """
    Member view for users with Member role.
    """
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

# Custom Permissions Views
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View to add a new book (requires can_add_book permission).
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit a book (requires can_change_book permission).
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book (requires can_delete_book permission).
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
