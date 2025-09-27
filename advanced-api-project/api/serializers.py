from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles serialization and deserialization of Book instances,
    including custom validation for publication year and proper error handling.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'publication_year', 'author', 'author_name',
            'isbn', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        Ensures the publication year is not in the future.
        """
        current_year = timezone.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}."
            )
        
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a reasonable year (1000 or later)."
            )
        
        return value

    def validate_title(self, value):
        """
        Custom validation for title field.
        Ensures the title is not empty and properly formatted.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Book title cannot be empty.")
        
        return value.strip()

    def validate_isbn(self, value):
        """
        Custom validation for ISBN field.
        Ensures ISBN format is correct if provided.
        """
        if value:
            # Remove hyphens and spaces
            clean_isbn = value.replace('-', '').replace(' ', '')
            if len(clean_isbn) not in [10, 13]:
                raise serializers.ValidationError(
                    "ISBN must be either 10 or 13 characters long."
                )
            return clean_isbn
        return value

    def validate(self, data):
        """
        Object-level validation for the entire Book instance.
        Performs cross-field validation and ensures data consistency.
        """
        # Check if author exists
        if 'author' in data:
            author = data['author']
            if not Author.objects.filter(id=author.id).exists():
                raise serializers.ValidationError(
                    "The specified author does not exist."
                )
        
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested book relationships.
    
    This serializer includes a nested BookSerializer to handle the
    one-to-many relationship between Author and Book models.
    """
    books = BookSerializer(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'books', 'books_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_books_count(self, obj):
        """
        Method to get the count of books for this author.
        """
        return obj.books.count()

    def validate_name(self, value):
        """
        Custom validation for name field.
        Ensures the author's name is not empty and properly formatted.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")
        
        return value.strip().title()

    def create(self, validated_data):
        """
        Override create method to handle nested book creation if needed.
        """
        author = Author.objects.create(**validated_data)
        return author

    def update(self, instance, validated_data):
        """
        Override update method to handle partial updates properly.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AuthorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Author model used in list views.
    
    This serializer provides a lightweight representation of authors
    without the full nested book data for better performance.
    """
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books_count', 'created_at', 'updated_at']

    def get_books_count(self, obj):
        """
        Method to get the count of books for this author.
        """
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Book model used in list views.
    
    This serializer provides a lightweight representation of books
    with basic author information for better performance.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'publication_year', 'author_name',
            'author', 'created_at', 'updated_at'
        ]