from django.forms import ModelForm

from order.models import *
from product.models import ItemInCart


class ItemInCartForm(ModelForm):
    class Meta:
        model = ItemInCart
        fields = ['quantity']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['payment']
