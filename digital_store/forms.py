from django import forms
from django_svg_image_form_field import SvgAndImageFormField
from digital_store.models import *



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'icon')


class BrandForm(forms.ModelForm):
    class Meta:
        fields = ('title', )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'quantity', 'price', 'color_name', 'discount', 'category', 'brand')
