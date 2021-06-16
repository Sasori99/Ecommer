from django.urls import path

from product.views import detailProduct, add_to_cart, shopping_cart, check_out, home, search_items, delete_item, \
    product_to_item_view

urlpatterns = [
    path('', home, name='home'),
    path('product-details/<int:item_id>', detailProduct, name='product-details'),
    path('add-to-cart/<int:id>', add_to_cart, name='add-to-cart'),
    path('shopping-cart', shopping_cart, name='shopping-cart'),
    path('check-out', check_out, name='check-out'),
    path('search-item', search_items, name='search-item'),
    path('delete-item-from-cart/<int:id>', delete_item, name='delete-item-from-cart'),
    path('product-to-item', product_to_item_view, name='product-to-item'),
    # path('', search_items, name='delete-item-from-cart'),
]