from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView

from order.forms import ItemInCartForm
from order.models import OrderStatusLogs, Payment
from staff.models import *
from product.models import *
from django.urls import reverse
# Create your views here.



def home(request):
    items = Item.objects.all().order_by('-id')[:4]
    context = {
        'items': items,
        'page': 'home'
    }
    return render(request, 'index.html', context)


def detailProduct(request, item_id):
    item = Item.objects.get(pk=item_id)
    cart = Cart.objects.filter(user=request.user)

    if len(cart) == 0:
        cart = Cart(user=request.user, cart_type="")
        cart.save()
    else:
        cart = Cart.objects.get(user=request.user)

    items_in_cart = ItemInCart.objects.filter(item=item, cart=cart).exclude(order__isnull=True)
    # order_status = OrderStatus.objects.get(status__exact="Đã hoàn thành")
    # order_status_logs = OrderStatusLogs.objects.filter(order__in=items_in_cart.order, order_status=order_status)
    can_comment = len(items_in_cart) > 0
    if request.method == 'POST' and can_comment:
        sentiment = Sentiment.objects.get(pk=1)
        commnet = Comment(customer=request.user, item=item, content=request.POST['content'],
                          rating=request.POST['rating'], sentiment=sentiment)
        commnet.save()
        return HttpResponseRedirect(reverse('product-details', kwargs={'item_id':item_id}))

    product = item.product
    product.price = int(product.price)
    if product.type == 1:
        product = Clothing.objects.get(pk=product.id)
    elif product.type == 2:
        product = Book.objects.get(pk=product.id)
    else:
        product = Electronic.objects.get(pk=product.id)
    comments = Comment.objects.filter(item=item)

    s = 0
    if len(comments) != 0:
        for comment in comments:
            s += int(comment.rating)
        s /= len(comments)
        s = round(s)

    context = {
        'item': item,
        'comments': comments,
        'products': product,
        'rating': s,
        'can_comment': can_comment,
    }

    return render(request, 'product_detail.html', context)


@login_required(login_url='/user/login')  # Check login
def add_to_cart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    item = Item.objects.get(pk=id)

    cart = Cart.objects.filter(user=current_user)
    if len(cart) == 0:
        cart = Cart(user=current_user)
        cart.save()
    else:
        cart = cart[0]

    data = ItemInCart.objects.filter(cart=cart, item=item, order=None)  # Check product in shopcart
    if len(data) != 0:
        control = 1
        # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ItemInCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ItemInCart.objects.get(cart=cart, item=item, order=None)  # Check product in shopcart
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ItemInCart(item_id=id, cart=cart, quantity=request.POST['quantity'])
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ItemInCart.objects.get(item_id=id, cart=cart, order=None)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ItemInCart(cart=cart, item_id=id, order=None)  # model ile bağlantı kur
            data.user_id = current_user.id
            data.item_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


@login_required(login_url='/user/login')  # Check login
def shopping_cart(request):
    current_user = request.user  # Access User Session information
    cart = Cart.objects.filter(user=current_user)
    if len(cart) == 0:
        cart = Cart(user=current_user)
        cart.save()
    else:
        cart = cart[0]

    if request.method == 'POST':
        for key in request.POST:
            if 'quantity' in key:
                item_in_cart = ItemInCart.objects.get(pk=int(key.split('_')[1]))
                item_in_cart.quantity = request.POST[key]
                item_in_cart.save()

        return redirect(check_out)

    shopcart = ItemInCart.objects.filter(cart=cart, order=None)
    total = 0
    for rs in shopcart:
        total += rs.item.price * rs.quantity
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart,
               'total': total,
               }
    return render(request, 'shopping_cart.html', context)


@login_required(login_url='/user/login')  # Check login
def check_out(request):
    current_user = request.user
    cart = Cart.objects.get(user_id=current_user.id)
    shopcart = ItemInCart.objects.filter(cart=cart, order=None)
    # address=Address.objects.get(pk=current_user.address)
    total = 0
    for rs in shopcart:
        total += rs.item.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        # return HttpResponse(request.POST.items())
        # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
        # ..............

        payment = Payment(amount=total, additional_fee=0)
        status = OrderStatus.objects.get(status='Đang duyệt')
        order = Order(sale_off=0, payment=payment, customer=current_user)
        order_log = OrderStatusLogs(order_status=status, order=order)

        payment.save()
        order.save()
        order_log.save()
        cart.save()
        for rs in shopcart:
            rs.order = order
            rs.save()

        # TODO : Remove from ProductInStock
        messages.success(request, "Your Order has been completed. Thank you ")
        return render(request, 'order_completed.html', {'order-code': order.id})

    context = {'shopcart': shopcart,
               'total': total,
               }
    return render(request, 'order_Form.html', context)


class ItemListView(ListView):
    paginate_by = 3
    model = Item


def search_items(request):
    if request.method != 'GET':
        items = Item.objects.all()
        items = Paginator(items, 3)
        page_number = request.GET.get('page')
        items = items.get_page(page_number)
        return render(request, 'items.html', {'items': items})
    else:
        filters = {}
        if 'product_name' in request.GET:
            filters['product__name__icontains'] = request.GET['product_name']
        if 'price' in request.GET:
            range = request.GET['price']

            if len(range) != 0:
                range = range.split('-')

                filters['price__gte'] = range[0].strip()[:-1]
                filters['price__lte'] = range[1].strip()[:-1]
        if 'type' in request.GET:
            filters['product__type'] = request.GET['type']

        items = Item.objects.filter(**filters)
        items = Paginator(items, 3)
        page_number = request.GET.get('page')
        items = items.get_page(page_number)
        return render(request, 'items.html', {'items': items})


@login_required(login_url='/user/login')  # Check login
def delete_item(request, id):
    ItemInCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopping-cart")


@login_required(login_url='/user/login')  # Check login
@staff_member_required
def product_to_item_view(request):
    item = Item.objects.all()

    products = Product.objects.exclude(id__in=Product.objects.filter(item__in=item))
    products_in_stock = ProductInStock.objects.filter(product__in=products)
    return render(request, 'product_to_item.html', {'products_in_stock': products_in_stock})
