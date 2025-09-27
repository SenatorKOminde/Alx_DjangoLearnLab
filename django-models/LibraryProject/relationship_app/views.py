from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic import DetailView
from .models import Book, Library, Author, Librarian
from django.contrib.auth.models import User
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login

# Function-based view: List all books
@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: Library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Authentication views (login, logout, register)
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

class RegisterView(FormView):
    template_name = 'relationship_app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Role-based access control
from .models import Author
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# Signal to create UserProfile automatically
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Role-based views
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Book permissions
from django.views.decorators.csrf import csrf_protect

@permission_required('relationship_app.can_add_book', raise_exception=True)
@csrf_protect
def add_book(request):
    return HttpResponse('Add Book - Permission Secured')

@permission_required('relationship_app.can_change_book', raise_exception=True)
@csrf_protect
def edit_book(request):
    return HttpResponse('Edit Book - Permission Secured')

@permission_required('relationship_app.can_delete_book', raise_exception=True)
@csrf_protect
def delete_book(request):
    return HttpResponse('Delete Book - Permission Secured')
