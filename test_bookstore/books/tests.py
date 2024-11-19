from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author


class BookListTestCase(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(first_name="John", last_name="Doe")
        self.book1 = Book.objects.create(title="Book 1", author=self.author1, count=10)

    def test_get_books(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("book-list"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["results"]), 1)
            self.assertLess(len(queries), 3)

    def test_post_book(self):
        data = {"title": "Book 2", "author_id": self.author1.id, "count": 5}
        response = self.client.post(reverse("book-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_filter_by_author(self):
        response = self.client.get(reverse("book-list"), {"author": self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Book 1")

    def test_filter_by_author_not_found(self):
        response = self.client.get(reverse("book-list"), {"author": 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_pagination(self):
        for i in range(15):
            Book.objects.create(title=f"Book {i}", author=self.author1, count=10)

        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # page size is 10

        next_page_url = response.data["next"]
        response = self.client.get(next_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), response.data["count"] - 10
        )  # remaining books

    def test_pagination_page_size(self):
        for i in range(15):
            Book.objects.create(title=f"Book {i}", author=self.author1, count=10)

        response = self.client.get(reverse("book-list"), {"page_size": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        next_page_url = response.data["next"]
        response = self.client.get(next_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_pagination_invalid_page_size(self):

        for i in range(15):
            Book.objects.create(title=f"Book {i}", author=self.author1, count=10)

        response = self.client.get(reverse("book-list"), {"page_size": 1001})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagination_empty_page(self):
        response = self.client.get(reverse("book-list"), {"page": 2})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookDetailTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="John", last_name="Doe")
        self.book = Book.objects.create(title="Book 1", author=self.author, count=10)

    def test_get_book(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book 1")

    def test_put_book(self):
        data = {"title": "Updated Book 1", "author_id": self.author.id, "count": 10}
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=self.book.id).title, "Updated Book 1")


class BookBuyTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="John", last_name="Doe")
        self.book = Book.objects.create(title="Book 1", author=self.author, count=10)

    def test_buy_book(self):
        response = self.client.post(reverse("book-buy", kwargs={"pk": self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=self.book.id).count, 9)

    def test_buy_out_of_stock_book(self):
        self.book.count = 0
        self.book.save()
        response = self.client.post(reverse("book-buy", kwargs={"pk": self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthorListTestCase(APITestCase):
    def test_get_authors(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post_author(self):
        data = {"first_name": "Jane", "last_name": "Doe"}
        response = self.client.post(reverse("author-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)


class AuthorDetailTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="John", last_name="Doe")

    def test_get_author(self):
        response = self.client.get(
            reverse("author-detail", kwargs={"pk": self.author.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")

    def test_put_author(self):
        data = {"first_name": "Updated John", "last_name": "Doe"}
        response = self.client.put(
            reverse("author-detail", kwargs={"pk": self.author.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Author.objects.get(id=self.author.id).first_name, "Updated John"
        )
