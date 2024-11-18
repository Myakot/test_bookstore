from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author

class BookListTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='John', last_name='Doe')
        self.book = Book.objects.create(title='Book 1', author=self.author, count=10)

    def test_get_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_book(self):
        data = {'title': 'Book 2', 'author_id': self.author.id, 'count': 5}
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

class AuthorListTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='John', last_name='Doe')

    def test_get_authors(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_author(self):
        data = {'first_name': 'Jane', 'last_name': 'Doe'}
        response = self.client.post(reverse('author-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
