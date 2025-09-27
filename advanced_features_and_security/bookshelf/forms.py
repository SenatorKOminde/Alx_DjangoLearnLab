from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """Form for creating and editing books with validation"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': '1000',
                'max': '2025'
            })
        }
    
    def clean_title(self):
        """Validate and sanitize book title"""
        title = self.cleaned_data.get('title')
        if title:
            # Remove any potential XSS content
            title = title.strip()
            if len(title) < 2:
                raise forms.ValidationError("Title must be at least 2 characters long.")
        return title
    
    def clean_author(self):
        """Validate and sanitize author name"""
        author = self.cleaned_data.get('author')
        if author:
            # Remove any potential XSS content
            author = author.strip()
            if len(author) < 2:
                raise forms.ValidationError("Author name must be at least 2 characters long.")
        return author
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        if year:
            if year < 1000 or year > 2025:
                raise forms.ValidationError("Publication year must be between 1000 and 2025.")
        return year