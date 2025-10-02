from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import ExampleForm

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Save logic here
            pass
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # Implementation for editing a book
    pass

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # Implementation for deleting a book
    pass
