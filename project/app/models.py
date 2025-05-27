# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Định nghĩa model Author để quản lý thông tin tác giả
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Tên tác giả, không được trùng
    birth_date = models.DateField()  # Ngày sinh
    biography = models.TextField(blank=True)  # Tiểu sử, có thể để trống

    # Meta class để định nghĩa metadata cho model
    class Meta:
        ordering = ['name']  # Sắp xếp theo tên mặc định
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    # Phương thức để trả về tên tác giả dưới dạng chuỗi
    def __str__(self):
        return self.name

    # Validation tùy chỉnh
    def clean(self):
        # Kiểm tra ngày sinh không được ở tương lai
        if self.birth_date > timezone.now().date():
            raise ValidationError("Ngày sinh không được ở tương lai.")

# Định nghĩa model Book để quản lý thông tin sách
class Book(models.Model):
    title = models.CharField(max_length=200)  # Tiêu đề sách
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # Mối quan hệ 1-n với Author
    publication_date = models.DateField()  # Ngày xuất bản
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sách
    isbn = models.CharField(max_length=13, unique=True)  # Mã ISBN, duy nhất

    class Meta:
        ordering = ['title']  # Sắp xếp theo tiêu đề

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    # Validation tùy chỉnh
    def clean(self):
        # Kiểm tra ISBN có đúng 13 ký tự
        if len(self.isbn) != 13 or not self.isbn.isdigit():
            raise ValidationError("ISBN phải là 13 chữ số.")
        # Kiểm tra giá không âm
        if self.price < 0:
            raise ValidationError("Giá không được âm.")