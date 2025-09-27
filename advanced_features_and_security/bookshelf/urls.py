from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('api/search/', views.book_search_api, name='book_search_api'),
]