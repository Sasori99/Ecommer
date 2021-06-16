from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from manufacturer.models import Manufacturer
from product.forms import ProductForm, ClothingForm
from product.models import Clothing, Book, Electronic, Item, Author, ProductInStock, Product


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    search_fields = ['name']
    exclude = ['status', 'type']


class ClothingAdmin(ProductAdmin):
    form = ClothingForm


class BookAdmin(ProductAdmin):
    form = ClothingForm


class ElectronicAdmin(ProductAdmin):
    form = ClothingForm


def make_item(modeladmin, request, queryset):
    sale_offs = []
    prices = []
    for x, y in request.POST.items():
        if 'sale_off' in x:
            sale_offs.append(y)

        elif 'price' in x:
            prices.append(y)
    sale_offs.sort()
    prices.sort()
    for i, product in enumerate(queryset):
        item = Item(sale_off=sale_offs[i], price=prices[i], product=product)
        item.save()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_tag', 'price_tag', 'sale_off_tag')
    actions = [make_item]

    def get_queryset(self, request):
        products = Product.objects.filter(id__in=Item.objects.all().values_list('product_id', flat=True))
        qs = super().get_queryset(request)
        return qs.exclude(id__in=products)

    def image_tag(self, obj):
        return mark_safe('<img src="/static/uploads/%s" width="150" height="150" />' % obj.image)

    def price_tag(self, obj):
        return mark_safe('<input type="text" name="price_' + str(obj.id) + '" value="' + str(obj.price) + '"/>')

    def sale_off_tag(self, obj):
        return mark_safe('<input type="text" name="sale_off_' + str(obj.id) + '"/>')

    image_tag.short_description = 'Ảnh'
    price_tag.short_description = 'Giá'
    sale_off_tag.short_description = 'Khuyến mãi'


admin.site.register(Clothing, ClothingAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Electronic, ElectronicAdmin)
admin.site.register(Author)
admin.site.register(ProductInStock)
admin.site.register(Product, ProductAdmin)
