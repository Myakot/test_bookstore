from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db import transaction
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class InvalidPageSizeError(Exception):
    pass


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        if page_size > self.max_page_size:
            raise InvalidPageSizeError("Invalid page size")
        return page_size


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.select_related("author").all().order_by("id")
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['author__first_name', 'author__last_name']
    filterset_fields = ['author']


class BookDetail(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookBuy(APIView):
    @transaction.atomic
    def post(self, request, pk):
        book = Book.objects.select_for_update().get(pk=pk)
        if book.count > 0:
            book.count -= 1
            book.save()
            return Response(
                {"message": "Book bought successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Book is out of stock"}, status=status.HTTP_400_BAD_REQUEST
            )


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
