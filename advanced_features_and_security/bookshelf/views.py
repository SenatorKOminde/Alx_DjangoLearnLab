from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book
from .forms import BookForm
import json

def book_list(request):
    """View to list all books - requires can_view permission"""
    if not request.user.has_perm('bookshelf.can_view'):
        messages.error(request, 'You do not have permission to view books.')
        return redirect('login')
    
    books = Book.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
def book_create(request):
    """View to create a new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Create New Book'
    })

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
def book_edit(request, book_id):
    """View to edit a book - requires can_edit permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': f'Edit {book.title}',
        'book': book
    })

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(["POST"])
@csrf_protect
def book_delete(request, book_id):
    """View to delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, id=book_id)
    book_title = book.title
    book.delete()
    messages.success(request, f'Book "{book_title}" deleted successfully!')
    return redirect('bookshelf:book_list')

def book_detail(request, book_id):
    """View to show book details - requires can_view permission"""
    if not request.user.has_perm('bookshelf.can_view'):
        messages.error(request, 'You do not have permission to view books.')
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# API endpoints for AJAX requests
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_search_api(request):
    """API endpoint for book search - requires can_view permission"""
    search_query = request.GET.get('q', '')
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )[:10]
        data = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
        return JsonResponse({'books': data})
    return JsonResponse({'books': []})