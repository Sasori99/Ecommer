from django.contrib import admin


# Register your models here.
from order.models import OrderStatusLogs

admin.site.register(OrderStatusLogs)

