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




class RegisterForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class LoginForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


