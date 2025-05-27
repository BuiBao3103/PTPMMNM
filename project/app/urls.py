from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet

# Khởi tạo router cho API
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)  # Đăng ký endpoint cho Author
router.register(r'books', BookViewSet)  # Đăng ký endpoint cho Book

# Định nghĩa URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Bao gồm tất cả các URL từ router
]