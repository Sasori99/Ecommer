from django.contrib import admin

# Register your models here.
from django.shortcuts import render
from django.utils.safestring import mark_safe

from product.forms import ProductForm, ClothingForm, BookForm, ElectronicForm
from product.models import Clothing, Book, Electronic, Item, Author, ProductInStock, Product, Manufacturer
from django.contrib import messages


def make_item(modeladmin, request, queryset):
    sale_offs = []
    prices = []
    for x, y in request.POST.items():
        if 'sale_off' in x:
            sale_offs.append(y)

        elif 'price' in x:
            prices.append(y)

    for i, product in enumerate(queryset):
        if len(Item.objects.filter(product=product)) == 0:
            item = Item(sale_off=sale_offs[i], price=prices[i], product=product)
            item.save()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_tag', 'price_tag', 'sale_off_tag')
    actions = [make_item]
    form = ProductForm
    search_fields = ['name']
    exclude = ['status', 'type']

    # def get_queryset(self, request):
    #     products = Product.objects.filter(id__in=Item.objects.all().values_list('product_id', flat=True))
    #     qs = super().get_queryset(request)
    #     return qs.exclude(id__in=products)

    def has_add_permission(self, request, obj=None):
        return False

    def image_tag(self, obj):
        return mark_safe('<img src="/static/uploads/%s" width="150" height="150" />' % obj.image)

    def price_tag(self, obj):
        return mark_safe('<input type="text" name="price_' + str(obj.id) + '" value="' + str(obj.price) + '"/>')

    def sale_off_tag(self, obj):
        return mark_safe('<input type="text" name="sale_off_' + str(obj.id) + '"/>')

    image_tag.short_description = 'Ảnh'
    price_tag.short_description = 'Giá'
    sale_off_tag.short_description = 'Khuyến mãi'


class ClothingAdmin(ProductAdmin):
    form = ClothingForm

    def has_add_permission(self, request, obj=None):
        return True


class BookAdmin(ProductAdmin):
    form = BookForm

    def has_add_permission(self, request, obj=None):
        return True


class ElectronicAdmin(ProductAdmin):
    form = ElectronicForm

    def has_add_permission(self, request, obj=None):
        return True


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_tag')

    def image_tag(self, obj):
        return mark_safe('<img src="/static/uploads/%s" width="150" height="150" />' % obj.product.image)

    def has_add_permission(self, request, obj=None):
        return False

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['product'].queryset = ProductInStock.objects.select_related('product')
        return super(ItemAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Item, ItemAdmin)
admin.site.register(Clothing, ClothingAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Electronic, ElectronicAdmin)
admin.site.register(Author)
admin.site.register(ProductInStock)
admin.site.register(Manufacturer)
admin.site.register(Product, ProductAdmin)
