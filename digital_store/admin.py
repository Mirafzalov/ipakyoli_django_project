from django.contrib import admin

from django.contrib import admin
from django.utils.safestring import mark_safe

# from .forms import CategoryForm
from tinymce.widgets import TinyMCE

from .models import *

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Brand)
# admin.site.register(Product)
# admin.site.register(Characteristic)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(ProfileUser)
admin.site.register(Cart)
admin.site.register(ProductCart)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1



############### Image getter
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'price', 'quantity', 'discount', 'color_name', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('category', 'brand', 'price')
    search_fields = ['title']
    list_editable = ('price', 'quantity', 'discount', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    inlines = [ProductImageInline]


    # def get_image(self, obj):
    #     # if self.images:
    #     return obj.images.url
    #


########### Icon getter needed to be done
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title', )}




@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title', )}




