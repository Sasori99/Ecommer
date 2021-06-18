from django.db import models

import user.models
from order.models import OrderStatus, Order

from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Address(models.Model):
    class Meta:
        verbose_name = _("Địa chỉ")
        verbose_name_plural = _("Địa chỉ")
    full_address = models.CharField(max_length=100, verbose_name= "Địa chỉ chi tiết")
    city = models.CharField(max_length=100, verbose_name= "Thành phố")
    country = models.CharField(max_length=100, verbose_name= "Đất nước")

    def __str__(self):
        return self.full_address + ', ' + self.city + ', ' + self.country


class Fullname(models.Model):
    class Meta:
        verbose_name = _("Họ và tên")
        verbose_name_plural = _("Họ và tên")
    firstname = models.CharField(max_length=100, verbose_name= "Tên")
    lastname = models.CharField(max_length=100, verbose_name= "Họ và tên đệm")

    def __str__(self):
        return self.firstname + " " + self.lastname


class Storage(models.Model):
    class Meta:
        verbose_name = _("Kho hàng")
        verbose_name_plural = _("Kho hàng")
    address = models.OneToOneField(Address, on_delete=models.CASCADE, verbose_name= "Địa chỉ")

    # chưa nối quan hệ trong bd class

    def __str__(self):
        return str(self.address)


class Staff(user.models.User):
    work_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True)

