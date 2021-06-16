from django.db import models

from shipment.models import Shipment


class OrderStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status


class Order(models.Model):
    sale_off = models.FloatField()
    payment = models.OneToOneField('payment.Payment', on_delete=models.CASCADE)
    customer = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Đơn hàng " + str(self.id)


class OrderStatusLogs(models.Model):
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    business_staff = models.ForeignKey('staff.Staff', on_delete=models.CASCADE, null=True)
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, null=True)
