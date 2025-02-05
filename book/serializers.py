from datetime import date
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.name')
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Book
        fields = '__all__'
    