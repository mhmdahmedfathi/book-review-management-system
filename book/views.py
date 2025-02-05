from rest_framework.response import Response
from rest_framework import status
from book_author.permissions import IsAuthorOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from .serializers import BookSerializer
from .models import Book

class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Book.objects.all().filter(author=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):
        self.permission_classes = []
        return self.retrieve(request, *args, **kwargs)
    