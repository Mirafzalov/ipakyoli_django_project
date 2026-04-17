from django.contrib import admin

from django.contrib import admin
from django.utils.safestring import mark_safe

# from .forms import CategoryForm
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(ModelProduct)
admin.site.register(Product)
# admin.site.register(Characteristic)
# admin.site.register(ImagesProduct)
# admin.site.register(Customer)
# admin.site.register(FavoriteProduct)
#
#
# admin.site.register(Cart)
# admin.site.register(ProductCart)
#
# admin.site.register(Delivery)
# admin.site.register(Region)
# admin.site.register(City)
#
#
# admin.site.register(Order)
# admin.site.register(ProductOrder)
#




#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'title', 'category_icon')
#     list_display_links = ('pk', 'title')
#     prepopulated_fields = {'slug': ('title', )}
#     form = CategoryForm
#
#     # Метод для отправки иконки
#     def category_icon(self, obj):
#         if obj.icon:
#             try:
#                 return mark_safe(f'<img src="{obj.icon.url}" width="30">')
#             except:
#                 return 'No icon'
#
#         else:
#             return 'No icon'
#
#
#
# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'title')
#     list_display_links = ('pk', 'title')
#     prepopulated_fields = {'slug': ('title', )}
#
#
#
#
# class CharacteristicInline(admin.TabularInline):
#     model = Characteristic
#     fk_name = 'product'
#     extra = 1
#
# class ImagesProductInline(admin.TabularInline):
#     model = ImagesProduct
#     fk_name = 'product'
#     extra = 1
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'title', 'price', 'quantity', 'discount', 'category', 'brand', 'product_image')
#     list_display_links = ('pk', 'title', )
#     prepopulated_fields = {'slug': ('title', )}
#     inlines = [CharacteristicInline, ImagesProductInline]
#     list_editable = ('price', 'quantity', 'discount')
#     list_filter = ('category', 'brand', 'price', )
#
#
#
#     def product_image(self, obj):
#         if obj.images:
#             try:
#                 return mark_safe(f'<img src="{obj.images.first().image.url}" width="60">')
#             except:
#                 return 'No image'
#
#         else:
#             return 'No image'