from django.urls import path

from . import views
from .views import order_list_view, order_details_view

urlpatterns = [
    # path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    # path('view_cart', views.view_cart, name='view_cart'),
    # path('delete_item/<int:id>', views.delete_item, name='delete_item'),
    # path('order/order_item', views.order_item, name='order_item'),
    path('view-orders-list', order_list_view, name='order-list-view'),
    path('view-orders-details/<int:order_log_id>', order_details_view, name='order-details-view')
]