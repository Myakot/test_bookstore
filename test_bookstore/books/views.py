from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class InvalidPageSizeError(Exception):
    pass

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        if page_size > self.max_page_size:
            raise InvalidPageSizeError('Invalid page size')
        return page_size

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Book.objects.all().order_by('id')
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author_id=author)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        page_size = request.GET.get('page_size')
        if page_size and int(page_size) > self.pagination_class.max_page_size:
            return JsonResponse({'error': 'Invalid page size'}, status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request, *args, **kwargs)

class BookDetail(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookBuy(APIView):
    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        if book.count > 0:
            book.count -= 1
            book.save()
            return Response({'message': 'Book bought successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Book is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
