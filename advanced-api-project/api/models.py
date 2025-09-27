from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model.
    """
    name = models.CharField(
        max_length=200,
        help_text="The full name of the author"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

    def clean(self):
        """
        Custom validation for the Author model.
        Ensures the author's name is not empty and properly formatted.
        """
        if not self.name or not self.name.strip():
            raise ValidationError("Author name cannot be empty.")
        
        # Capitalize first letter of each word
        self.name = self.name.strip().title()


class Book(models.Model):
    """
    Book model representing a book with its details.
    
    This model establishes a many-to-one relationship with the Author model,
    meaning one author can have multiple books, but each book has one author.
    """
    title = models.CharField(
        max_length=300,
        help_text="The title of the book"
    )
    publication_year = models.IntegerField(
        help_text="The year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author of this book"
    )
    isbn = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        help_text="International Standard Book Number (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # Ensure unique combination of title and author
        unique_together = ['title', 'author']

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def clean(self):
        """
        Custom validation for the Book model.
        Ensures publication year is not in the future and title is not empty.
        """
        current_year = timezone.now().year
        
        if not self.title or not self.title.strip():
            raise ValidationError("Book title cannot be empty.")
        
        if self.publication_year > current_year:
            raise ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}."
            )
        
        if self.publication_year < 1000:
            raise ValidationError(
                "Publication year must be a reasonable year (1000 or later)."
            )
        
        # Clean and format the title
        self.title = self.title.strip()
        
        # Clean ISBN if provided
        if self.isbn:
            self.isbn = self.isbn.strip().replace('-', '').replace(' ', '')
            if len(self.isbn) not in [10, 13]:
                raise ValidationError(
                    "ISBN must be either 10 or 13 characters long."
                )

    def save(self, *args, **kwargs):
        """
        Override save method to ensure validation is always run.
        """
        self.full_clean()
        super().save(*args, **kwargs)