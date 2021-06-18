from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    address = models.ForeignKey('staff.Address', on_delete=models.CASCADE, null=True)


class Cart(models.Model):
    cart_type = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)