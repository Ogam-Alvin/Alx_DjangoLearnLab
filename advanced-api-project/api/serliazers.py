from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


# BookSerializer handles serialization of Book objects
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation to prevent future publication years
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# AuthorSerializer serializes Author data
# Includes a nested BookSerializer for related books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer dynamically pulls all related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
