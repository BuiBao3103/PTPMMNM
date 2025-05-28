from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone
class AuthorSerializer(serializers.ModelSerializer):
    # Thêm trường books để hiển thị danh sách sách của tác giả
    books = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'biography', 'books']  # Các trường sẽ được serialize

    # Validation tùy chỉnh cho name
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Tên tác giả phải có ít nhất 2 ký tự.")
        return value

# Serializer cho Book
class BookSerializer(serializers.ModelSerializer):
    # Sử dụng StringRelatedField để hiển thị tên tác giả thay vì ID
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='author')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'publication_date', 'price', 'isbn']

    # Validation cho publication_date
    def validate_publication_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Ngày xuất bản không được ở tương lai.")
        return value