from django import forms

from product.models import Product, Clothing, Book, Electronic


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['type']


class ClothingForm(ProductForm):
    class Meta:
        model = Clothing
        exclude = ['type']


class BookForm(ProductForm):
    class Meta:
        model = Book
        exclude = ['type']


class ElectronicForm(ProductForm):
    class Meta:
        model = Electronic
        exclude = ['type']
