from django.db import models

from django.utils.translation import ugettext_lazy as _


class OrderStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status


class Payment(models.Model):
    amount = models.FloatField(max_length=100)
    additional_fee = models.FloatField(max_length=100)

    def __str__(self):
        return "Tiền mặt " + str(self.amount) + ", phụ phí " + str(self.additional_fee)


class Order(models.Model):
    class Meta:
        verbose_name = _("Đơn hàng")
        verbose_name_plural = _("Đơn hàng")

    sale_off = models.FloatField(verbose_name="Giảm giá")
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, verbose_name="Thanh toán")
    customer = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, verbose_name="Khách hàng")

    def __str__(self):
        return "Đơn hàng " + str(self.id)


class ShipmentStatus(models.Model):
    status = models.CharField(max_length=100)


class Shipment(models.Model):
    ship_date = models.DateTimeField(max_length=100)
    receive_date = models.DateTimeField(max_length=100)


class ShipmentStatusLogs(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    shipment_status = models.ForeignKey(ShipmentStatus, on_delete=models.DO_NOTHING)
    shipment = models.ForeignKey(Shipment, on_delete=models.DO_NOTHING)


class DomesticShip(Shipment):
    distance = models.BigIntegerField()
    district = models.CharField(max_length=100)


class GlobalShip(Shipment):
    country = models.CharField(max_length=100)
    delivery_type = models.CharField(max_length=100)


class OrderStatusLogs(models.Model):
    class Meta:
        verbose_name = _("Nhật ký trạng thái đơn hàng")
        verbose_name_plural = _("Nhật ký trạng thái đơn hàng")

    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, verbose_name="Trạng thái đơn hàng")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Đơn hàng")
    business_staff = models.ForeignKey('staff.Staff', on_delete=models.CASCADE, null=True,
                                       verbose_name="Nhân viên kinh doanh")
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, null=True, verbose_name="Giao hàng")


class Notification(models.Model):
    content = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)


class CreditCard(models.Model):
    credit_number = models.BigIntegerField()
    customer = models.ForeignKey('user.User', on_delete=models.CASCADE)


class CreditCardPayment(Payment):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)

    def __str__(self):
        return "Thẻ " + str(self.amount) + ", phụ phí " + str(self.additional_fee)


class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
