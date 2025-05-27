from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# ViewSet cho Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()  # Truy vấn tất cả tác giả
    serializer_class = AuthorSerializer

    # Tùy chỉnh phương thức list để hỗ trợ tìm kiếm
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Tìm kiếm theo tên nếu có query parameter 'search'
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# ViewSet cho Book
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Xử lý truy vấn liên bảng
    @action(detail=False, methods=['get'])
    def filter_by_author(self, request):
        author_id = request.query_params.get('author_id')
        if not author_id:
            return Response({"error": "Vui lòng cung cấp author_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Truy vấn liên bảng: lấy sách theo tác giả
            books = Book.objects.filter(author__id=author_id).select_related('author')
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response({"error": "Tác giả không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

    # Xử lý lỗi trong phương thức create
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Đã có lỗi xảy ra"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)