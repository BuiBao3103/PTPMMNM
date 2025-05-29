# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, CategoryViewSet

# Khởi tạo router để tự động tạo URL cho ViewSet (thuộc yêu cầu: Xây dựng API)
router = DefaultRouter()
# Đăng ký endpoint cho books (CRUD và custom action low_stock)
router.register(r'books', BookViewSet)
# Đăng ký endpoint cho authors (CRUD)
router.register(r'authors', AuthorViewSet)
# Đăng ký endpoint cho categories (CRUD)
router.register(r'categories', CategoryViewSet)

# Định nghĩa URL patterns
urlpatterns = [
    path('', include(router.urls)),
]