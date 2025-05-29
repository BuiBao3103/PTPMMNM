# views.py
from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer

# ViewSet cho Book: Xử lý API cho sách (thuộc yêu cầu: Viết ViewSet, xây dựng API, xử lý truy vấn liên bảng và lỗi)
class BookViewSet(viewsets.ModelViewSet):
    # Queryset mặc định: Lấy tất cả sách
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Tùy chỉnh queryset để hỗ trợ lọc và tối ưu hóa truy vấn liên bảng
    def get_queryset(self):
        # Tối ưu hóa truy vấn với select_related (cho ForeignKey) và prefetch_related (cho ManyToMany)
        queryset = Book.objects.all().select_related('category').prefetch_related('authors')
        # Lấy tham số query từ request để lọc dữ liệu
        title = self.request.query_params.get('title', None)
        category = self.request.query_params.get('category', None)
        author = self.request.query_params.get('author', None)

        # Lọc theo tiêu đề sách (không phân biệt hoa thường)
        if title:
            queryset = queryset.filter(title__icontains=title)
        # Lọc theo tên danh mục (truy vấn liên bảng qua ForeignKey)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        # Lọc theo tên tác giả (truy vấn liên bảng qua ManyToMany)
        if author:
            queryset = queryset.filter(authors__name__icontains=author)

        return queryset

    # Custom action: Lấy sách có số lượng tồn kho thấp (thuộc yêu cầu: Xây dựng API để truy vấn)
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        # Lấy tham số threshold từ query params, mặc định là 5
        threshold = request.query_params.get('threshold', 5)
        try:
            threshold = int(threshold)
            # Lọc sách có số lượng tồn kho nhỏ hơn hoặc bằng threshold
            books = Book.objects.filter(stock__lte=threshold)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        except ValueError:
            # Xử lý lỗi khi threshold không phải số (thuộc yêu cầu: Xử lý lỗi trong API)
            return Response(
                {"error": "Threshold phải là một số"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Ghi đè phương thức create để xử lý lỗi khi tạo sách (thuộc yêu cầu: Xây dựng API để tạo, xử lý lỗi)
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            # Trả về lỗi 400 nếu validation thất bại
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# ViewSet cho Author: Xử lý API cho tác giả (thuộc yêu cầu: Viết ViewSet, xây dựng API)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# ViewSet cho Category: Xử lý API cho danh mục (thuộc yêu cầu: Viết ViewSet, xây dựng API)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer