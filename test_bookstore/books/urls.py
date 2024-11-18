from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('books/<int:pk>/buy/', views.BookBuy.as_view(), name='book-buy'),
    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
]
