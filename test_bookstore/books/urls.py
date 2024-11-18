from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('authors/', views.AuthorList.as_view()),
]
