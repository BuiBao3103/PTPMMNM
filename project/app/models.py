# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Model Category: Đại diện cho danh mục sách (thuộc yêu cầu: Viết model với field, mối quan hệ, phương thức và validation)


class Category(models.Model):
    # Trường name: Tên danh mục, giới hạn 100 ký tự, phải duy nhất để tránh trùng lặp
    name = models.CharField(max_length=100, unique=True)
    # Trường description: Mô tả danh mục, có thể để trống
    description = models.TextField(blank=True)

    # Phương thức __str__: Trả về tên danh mục khi in object, giúp dễ đọc trong admin hoặc console
    def __str__(self):
        return self.name


# Model Author: Đại diện cho thông tin tác giả (thuộc yêu cầu: Viết model)
class Author(models.Model):
    # Trường name: Tên tác giả, giới hạn 100 ký tự, bắt buộc
    name = models.CharField(max_length=100)
    # Trường birth_date: Ngày sinh, có thể để trống hoặc null
    birth_date = models.DateField(null=True, blank=True)
    # Trường nationality: Quốc tịch, có thể để trống
    nationality = models.CharField(max_length=50, blank=True)

    # Phương thức __str__: Trả về tên tác giả khi in object
    def __str__(self):
        return self.name

# Model Book: Đại diện cho thông tin sách (thuộc yêu cầu: Viết model với mối quan hệ và validation)


class Book(models.Model):
    # Trường title: Tiêu đề sách, giới hạn 200 ký tự
    title = models.CharField(max_length=200)
    # Trường category: Quan hệ ForeignKey với Category, khi danh mục bị xóa thì sách cũng bị xóa
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='books')
    # Trường authors: Quan hệ ManyToMany với Author, một sách có thể có nhiều tác giả
    authors = models.ManyToManyField(Author, related_name='books')
    # Trường published_date: Ngày xuất bản sách
    published_date = models.DateField()
    # Trường price: Giá sách, định dạng số thập phân với 10 chữ số và 2 chữ số thập phân
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Trường stock: Số lượng tồn kho, chỉ cho phép số nguyên không âm
    stock = models.PositiveIntegerField(default=0)

    # Phương thức clean: Validation dữ liệu, kiểm tra ngày xuất bản không được là tương lai
    def clean(self):
        if self.published_date > timezone.now().date():
            raise ValidationError("Ngày xuất bản không được là tương lai.")

    # Phương thức __str__: Trả về tiêu đề sách khi in object
    def __str__(self):
        return self.title

    # Meta class: Cấu hình bổ sung cho model
    class Meta:
        # Sắp xếp mặc định theo tiêu đề sách
        ordering = ['title']
