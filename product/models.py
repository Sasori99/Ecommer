from django.db import models
from django.utils.safestring import mark_safe

from user.models import User, Cart

from django.utils.translation import ugettext_lazy as _


class Manufacturer(models.Model):
    class Meta:
        verbose_name = _("Nhà sản xuất")
        verbose_name_plural = _("Nhà sản xuất")

    name = models.CharField(max_length=100, verbose_name="Tên")
    ad = models.OneToOneField('staff.Address', on_delete=models.CASCADE, verbose_name="Địa chỉ")

    def __str__(self):
        return self.name + " " + str(self.ad)


class Product(models.Model):
    class Meta:
        verbose_name = _("Sản phẩm")
        verbose_name_plural = _("Sản phẩm")

    TYPE = (
        ('1', 'Quần Áo'),
        ('2', 'Sách'),
        ('3', 'Điện Tử')
    )
    STATUS = (
        ('True', 'Đang Kinh Doanh'),
        ('False', 'Ngừng Kinh Doanh'),
    )

    name = models.CharField(max_length=100, verbose_name="Tên")
    price = models.FloatField(verbose_name="Giá mua")
    image = models.ImageField(verbose_name="Ảnh")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Nhà sản xuất")
    type = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default=True, verbose_name="Trạng thái")

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format('/static' + self.image.url))
        else:
            return ""
    # def category(self):
    #     if self.TYPE


class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductInStock(models.Model):
    class Meta:
        verbose_name = _("Nhập kho sản phẩm")
        verbose_name_plural = _("Nhập kho sản phẩm")

    stock = models.IntegerField(verbose_name="Lượng tồn kho")
    storage = models.ForeignKey('staff.Storage', on_delete=models.CASCADE, verbose_name="Kho")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")

    def __str__(self):
        return str(self.product) + ", kho " + str(self.storage)


# Create your models here.
class Genre(models.Model):
    genre = models.CharField(max_length=100)


class BookStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status


class Author(models.Model):
    class Meta:
        verbose_name = _("Tác giả")
        verbose_name_plural = _("Tác giả")

    sex = models.CharField(max_length=100, verbose_name="Giới tính")
    age = models.IntegerField(verbose_name="Tuổi")
    fullname = models.ForeignKey('staff.Fullname', on_delete=models.CASCADE, verbose_name="Họ và tên")
    organization = models.CharField(max_length=100, verbose_name="Tổ chức")

    def __str__(self):
        return " Tác giả số " + str(self.id) + ", " + str(self.fullname) + ", Tổ chức " + self.organization


class Book(Product):
    class Meta:
        verbose_name = _("Sách")
        verbose_name_plural = _("Sách")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 2

    book_status = models.ForeignKey(BookStatus, on_delete=models.CASCADE, verbose_name="Tình trạng")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Tác giả")


class BookGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Electronic(Product):
    class Meta:
        verbose_name = _("Đồ điện tử")
        verbose_name_plural = _("Đồ điện tử")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 3

    desc = models.CharField(max_length=100, verbose_name="Mô tả")


class Appliance(Electronic):
    width = models.CharField(max_length=100)
    height = models.FloatField()
    length = models.FloatField()
    type_of_appliance = models.CharField(max_length=100)


class Mobile(Electronic):
    dimension = models.FloatField()
    device_type = models.CharField(max_length=100)


class ClothingType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Clothing(Product):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 1

    class Meta:
        verbose_name = _("Quần áo")
        verbose_name_plural = _("Quần áo")

    material = models.CharField(max_length=100, verbose_name="Chất")
    desc = models.CharField(max_length=100, verbose_name="Mô tả")
    type_of_clothing = models.ForeignKey(ClothingType, on_delete=models.CASCADE, verbose_name="Loại")


class Item(models.Model):
    class Meta:
        verbose_name = _("Sản phẩm đang bán")
        verbose_name_plural = _("Sản phẩm đang bán")

    sale_off = models.FloatField(verbose_name="Khuyến mãi")
    price = models.FloatField(verbose_name="Giá bán")
    product = models.OneToOneField('product.Product', on_delete=models.DO_NOTHING)


class ItemInCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = _("Nhà sản xuất")
        verbose_name_plural = _("Nhà sản xuất")


class Sentiment(models.Model):
    sentiment = models.CharField(max_length=20)


class Comment(models.Model):
    content = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()
    sentiment = models.ForeignKey(Sentiment, on_delete=models.DO_NOTHING)
