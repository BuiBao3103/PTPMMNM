# serializers.py
from rest_framework import serializers
from .models import Category, Author, Book

# Serializer cho Author: Chuyển đổi dữ liệu Author thành JSON (thuộc yêu cầu: Viết serializer)
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # Các trường sẽ được serialize để trả về hoặc nhận từ API
        fields = ['id', 'name', 'birth_date', 'nationality']

# Serializer cho Category: Chuyển đổi dữ liệu Category thành JSON (thuộc yêu cầu: Viết serializer)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Các trường sẽ được serialize
        fields = ['id', 'name', 'description']

# Serializer cho Book: Chuyển đổi dữ liệu Book, xử lý mối quan hệ và validation (thuộc yêu cầu: Viết serializer)
class BookSerializer(serializers.ModelSerializer):
    # Nested serializer: Hiển thị thông tin chi tiết của category (read-only)
    category = CategorySerializer(read_only=True)
    # Nhận category_id để tạo/cập nhật sách (write-only)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    # Nested serializer: Hiển thị thông tin chi tiết của authors (read-only)
    authors = AuthorSerializer(many=True, read_only=True)
    # Nhận danh sách author_ids để tạo/cập nhật sách (write-only)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, source='authors', write_only=True
    )

    class Meta:
        model = Book
        # Các trường sẽ được serialize, bao gồm cả trường read-only và write-only
        fields = ['id', 'title', 'category', 'category_id', 'authors', 'author_ids',
                 'published_date', 'price', 'stock']

    # Validation tùy chỉnh: Đảm bảo giá sách phải lớn hơn 0
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Giá phải lớn hơn 0")
        return value