from datetime import date
from rest_framework import serializers

from book.models import Book
from user.models import User
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    book = serializers.ReadOnlyField(source='book.title')
    created_at = serializers.DateTimeField(default=date.today)

    class Meta:
        model = Review
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    
    class Meta:
        model = Review
        exclude = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        if validated_data['book'].author == validated_data['user']:
            raise serializers.ValidationError("You can't review your own book")
        return Review.objects.create(**validated_data)