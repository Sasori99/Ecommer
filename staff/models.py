from django.db import models

import user.models
from order.models import OrderStatus, Order


# Create your models here.


class Address(models.Model):
    full_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.full_address + ', ' + self.city + ', ' + self.country


class Fullname(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname + " " + self.lastname


class Storage(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    # chưa nối quan hệ trong bd class

    def __str__(self):
        return str(self.address)


class Staff(user.models.User):
    work_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True)

