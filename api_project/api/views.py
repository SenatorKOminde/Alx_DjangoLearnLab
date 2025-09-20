
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# All API views require authentication by default (see settings.py REST_FRAMEWORK config)
# You can override or extend permissions per view as needed.

# ListAPIView for listing books (requires authentication)
class BookList(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]  # Only authenticated users can access

# ModelViewSet for CRUD operations (requires authentication)
class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]  # Only authenticated users can access
