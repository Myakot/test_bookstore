from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view(), name='book-list'),
    path('authors/', views.AuthorList.as_view(), name='author-list'),
]
