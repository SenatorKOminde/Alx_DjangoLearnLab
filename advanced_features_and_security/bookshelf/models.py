from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"