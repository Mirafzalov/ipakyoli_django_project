from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
# Create your views here.
from django.views.generic import DetailView, ListView
from django.contrib import messages
from digital_store.forms import *
from digital_store.models import Product, Category, ProfileUser


# class MainPage(ListView):
#     model = Category
#     context_object_name = 'categories'
#     template_name = 'digital_store/index.html'
#     extra_context = {'title': 'Digital Store МАГАЗИН ТЕХНИКИ'}
#
#


def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'title': 'Digital Store',
        'products': products,
        'categories': categories,
        'brands': brands,
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


def product_filter_view(request):
    products = Product.objects.all()

    category = request.GET.get('category')
    brand = request.GET.get('brand')
    price = request.GET.get('price')

    if category:
        products = products.filter(category__slug=category)

    if brand:
        products = products.filter(brand__slug=brand)

    if price:
        products = products.filter(price__lte=price)

    context = {
        'title': 'Digital Store',
        'products': products,
    }

    return render(request, 'digital_store/products.html', context)


# LOGIN AND REGISTER

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect('home')

        messages.error(request, 'Неверный логин или пароль')

    else:
        form = LoginForm()

    return render(request, 'digital_store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data['phone']
            if User.objects.filter(username=phone).exists():
                form.add_error('phone', 'Этот номер уже используется')
            else:
                user = form.save(commit=False)
                user.username = phone
                user.save()
                ProfileUser.objects.create(user=user)
                login(request, user)
                return redirect('home')

        else:
            messages.error(request,
                           'Ошибка при регистрации, пожалуйста заполните все поля или введите 8 значный пароль!')

    else:
        form = RegisterForm()

    return render(request, 'digital_store/register.html', {'form': form})


def profile_user_view(request):
    user = request.user
    profile = ProfileUser.objects.get(user=user)
    edit = request.GET.get('edit') == 'true'

    error = None

    if request.method == 'POST':
        phone = request.POST.get('phone')
        if User.objects.exclude(id=user.id).filter(username=phone).exists():
            error = 'Этот номер уже используется'

        else:
            user.username = phone
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')

            if request.FILES.get('image'):
                profile.image = request.FILES.get('image')

            user.save()
            profile.save()

            return redirect('profile')  # ✔ only after success

    return render(request, 'digital_store/profile.html', {
        'profile': profile,
        'edit': edit,
        'user': user,
        'error': error,
    })




def edit_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'digital_store/settings.html', {'form': form})



########################################################################################################


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

# # Login and Register
#
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('')
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         user = form
#         return redirect('main')
#
# def logout_view(request):
#     logout(request)
#     return redirect('main')
#
#
# def register_view(request):
#     if request.user.is_authenticated:
#         return redirect('login')
#     else:
#         if request.method == 'POST':
#             form = RegisterForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 return redirect('')
#         else:
#             form = RegisterForm()
#
#     return render(request, 'digital_store/register.html', {'title': 'Регистрация',  'reg_form': form})
#
#
