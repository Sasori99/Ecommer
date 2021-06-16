from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView

from order.models import OrderStatusLogs
from product.models import ItemInCart
from staff.models import *


class OrdertListView(ListView):
    paginate_by = 3
    model = Order


@login_required(login_url='/user/login')  # Check login
def order_list_view(request):
    orders = OrderStatusLogs.objects.filter(order__customer=request.user)
    paginator = Paginator(orders, 2)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'order_list.html', {'page_obj': page_obj})


@login_required(login_url='/user/login')  # Check login
def order_details_view(request, order_log_id):
    order_log = OrderStatusLogs.objects.get(pk=order_log_id)
    ordered_items = ItemInCart.objects.filter(order=order_log.order)
    if order_log.order.customer != request.user:
        return render(request, '', {})
    return render(request, 'order_details.html', {'order_log': order_log, 'ordered_items': ordered_items})
