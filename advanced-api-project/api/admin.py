from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for Author model.
    
    Provides a comprehensive admin interface for managing authors
    with optimized display and filtering options.
    """
    list_display = ['name', 'books_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    def books_count(self, obj):
        """
        Display the number of books for this author.
        """
        return obj.books.count()
    books_count.short_description = 'Books Count'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    
    Provides a comprehensive admin interface for managing books
    with optimized display, filtering, and search capabilities.
    """
    list_display = ['title', 'author', 'publication_year', 'isbn', 'created_at']
    list_filter = ['publication_year', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'author__name', 'isbn']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-publication_year', 'title']
    raw_id_fields = ['author']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
        ('Additional Information', {
            'fields': ('isbn',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize queries for the admin interface.
        """
        return super().get_queryset(request).select_related('author')