from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
# Create your views here.
from django.views.generic import DetailView, ListView

from digital_store.forms import *
from digital_store.models import Product, Category



#
# class MainPage(ListView):
#     model = Category
#     context_object_name = 'categories'
#     template_name = 'digital_store/index.html'
#     extra_context = {'title': 'Digital Store МАГАЗИН ТЕХНИКИ'}
#
#



def product_list_view(request):
    products = Product.objects.all()
    context = {
        'title': 'Digital Store',
        'products': products
    }

    return render(request, 'digital_store/index.html', context)



def product_detail_view(request, slug, id):
    # It is for getting the product detail
    product = get_object_or_404(Product, id=id)
    # It is for getting similar products
    products = Product.objects.filter(category=product.category).exclude(id=product.id)

    context = {
        'products': products,
        'product': product
    }

    if product.slug != slug:
        return redirect('product_detail', slug=product.slug, id=product.id)

    return render(request, 'digital_store/product_detail.html', context)



####################################################
def get_category(request):
    categories = Category.objects.all().order_by('id')
    return render(request, 'digital_store/form_list.html', {'categories': categories, 'title': 'title'})



def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "GET":
        category.delete()
    return redirect('category_list')

def get_category_detail(request, id):
    if request.method == 'GET':
        category = Category.objects.get(id=id)
        return render(request, 'digital_store/category_detail.html', {'category': category})
    elif request.method == 'POST':
        category = get_object_or_404(Category, id=id)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            print(request.FILES)
            print(form.cleaned_data)
            form.save()
        else:
            print("ERROR:", form.errors)

        return redirect('category_list')



def add_category(request):
    form = CategoryForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('category_list')

    return render(request, 'digital_store/add_form.html', {
        'form': form
    })


# Login and Register

def login_view(request):
    if request.user.is_authenticated:
        return redirect('')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = form
        return redirect('main')

def logout_view(request):
    logout(request)
    return redirect('main')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('')
        else:
            form = RegisterForm()

    return render(request, 'digital_store/register.html', {'title': 'Регистрация',  'reg_form': form})



