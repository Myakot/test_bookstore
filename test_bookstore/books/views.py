from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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
