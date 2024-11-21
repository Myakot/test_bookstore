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
    filterset_fields = ['author']
    search_fields = ['author_name']

    def get_queryset(self):
        queryset = Book.objects.select_related("author").all().order_by("id")
        if "author" in self.request.GET:
            queryset = queryset.filter(author_id=self.request.GET["author"])
        return queryset

    def get_object(self):
        cache_key = "book_{}".format(self.kwargs["pk"])
        obj = cache.get(cache_key)
        if obj is None:
            obj = super().get_object()
            cache.set(cache_key, obj)
        return obj


class BookDetail(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookBuy(APIView):
    @transaction.atomic
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
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
