from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
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




class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=False, widget=forms.TextInput())

    last_name = forms.CharField(label=False, widget=forms.TextInput())

    email = forms.EmailField(label=False, widget=forms.EmailInput())

    password1 = forms.CharField(label=False, widget=forms.PasswordInput())

    password2 = forms.CharField(label=False, widget=forms.PasswordInput())

    phone = forms.CharField(label=False, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = UsernameField(label=False, widget=forms.TextInput())

    password = forms.CharField(label=False, widget=forms.PasswordInput())


