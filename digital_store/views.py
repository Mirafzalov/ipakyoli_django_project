from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
# Create your views here.
from django.views.generic import DetailView, ListView
from django.contrib import messages
from humanize import intcomma

from digital_store.forms import *
from digital_store.models import Product, Category, Brand

from digital_store.utils import CartAction

from digital_store.templatetags.user_roles import is_seller, is_buyer 

# class MainPage(ListView):
#     model = Category
#     context_object_name = 'categories'
#     template_name = 'digital_store/index.html'
#     extra_context = {'title': 'Digital Store МАГАЗИН ТЕХНИКИ'}



def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'title': 'Digital Store',
        'products': products,
        # 'categories': categories,
        # 'brands': brands,
    }

    return render(request, 'digital_store/index.html', context)


def product_detail_view(request, slug, id):
    # It is for getting the product detail
    product = get_object_or_404(Product, id=id)
    # product = Product.objects.get(id=id)
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
            role = form.cleaned_data['role']
            if User.objects.filter(username=phone).exists():
                form.add_error('phone', 'Этот номер уже используется')
            else:
                user = form.save(commit=False)
                user.username = phone
                user.save()
                if role == 'buyer':
                    BuyerProfile.objects.create(user=user)
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
    if is_buyer(user):
        profile = BuyerProfile.objects.get(user=user)
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


            user.save()
            profile.save()

            return redirect('profile')

    orders = Order.objects.filter(buyer=profile)
    total_orders = orders.count()
    cart = Cart.objects.get(buyer=profile)
    cart_products = ProductCart.objects.filter(cart=cart)
    cart_total_products = 0
    for p in cart_products:
        print(p.quantity)
        cart_total_products += p.quantity

    return render(request, 'digital_store/profile.html', {
        'profile': profile,
        'edit': edit,
        'user': user,
        'error': error,
        'total_orders': total_orders,
        'cart_total_products': cart_total_products  ,
    })




# Seller Profile
def seller_profile(request, id):
    seller = SellerProfile.objects.get(id=id)
    products = Product.objects.filter(seller=seller)
    total_products = products.count()
    
    edit = request.GET.get("edit") == "true"
    
    if request.user.is_authenticated:
        
        error = None
        
        if request.method == 'POST' and  is_seller(request.user):
            edit = request.GET.get('edit') == 'true'
            
            store_name=request.POST.get('store_name')
            if SellerProfile.objects.exclude(id=id).filter(store_name=store_name):
                error = '- Это название уже используется'
                
            else:
                seller.store_name = request.POST.get('store_name')
            
                seller.description = request.POST.get('description')
            
                if request.FILES.get('logo'):
                    seller.logo = request.FILES['logo']
                
                if request.FILES.get('banner'):
                    seller.banner = request.FILES['banner']
                    
                seller.save()
                
                return redirect('seller_profile', id=seller.id)

            
        

        context = {
            'seller_profile': seller,
            'products': products,
            'total_products': total_products,
            'edit': edit,
            'error': error
        }
            
        return render(request, 'digital_store/seller_profile.html', context)


####### Seller Dashboard

def seller_dashboard(request):
    if request.user.is_authenticated and is_seller(request.user):


        seller = request.user.seller_profile
        
        products = Product.objects.filter(seller=seller)
        
        product_total = 0
        active_total = 0
        for p in products:
            if p.is_active:
                  active_total += 1
            product_total += p.quantity
                 
        
        context = {
            'products': products, 
            'product_total': product_total, 
            'active_total': active_total,
            'user': request.user,
        }
    
        return render(request, 'digital_store/seller_dashboard.html', context)
    
    return redirect('home')


def add_product(request):
    if request.user.is_authenticated and is_seller(request.user):
        
        if request.method == 'POST':
            form = ProductForm(request.POST)
            
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user.seller_profile
                product.save()

                images = request.FILES.getlist('images')
                
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
                    
                    
                return redirect('seller_dashboard')
            
        else:
            form = ProductForm()
            
            
        categories = Category.objects.all()
        brands = Brand.objects.all()
        
        context={
            'form': form,
            'categories': categories,
            'brands': brands
        }
        return render(request, 'digital_store/product_form.html', context)        
    
    
    return redirect('home')




def edit_product(request, id):
    if request.user.is_authenticated and is_seller(request.user):
        seller = request.user.seller_profile
        product = get_object_or_404(Product, seller=seller, id=id)
        if request.method == 'POST':    
            form = ProductForm(request.POST, request.FILES, instance=product)
            
            if form.is_valid():
                product = form.save()
                images = request.FILES.getlist('images')
                
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
                    
                return redirect('seller_dashboard')
        
        else:
            form = ProductForm(instance=product)
        
        categories = Category.objects.all()
        brands = Brand.objects.all()
        
        context = {
            'form': form,
            'categories': categories,
            'brands': brands,
            'product': product
        }
        return render(request, 'digital_store/product_form.html', context)
    
    
    else:
        return redirect('home')        

            
                
    
def delete_product(request, id):
    if request.user.is_authenticated and is_seller(request.user):
        seller = request.user.seller_profile
        product = get_object_or_404(Product, seller=seller, id=id)
        product.delete()
        
    return redirect('seller_dashboard')
    
############
    

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



####### Корзина
# def add_cart_view(request, slug, action):
#     if is_buyer(request.user):
#         cart_class = CartAddDelete(request)
#         cart_class = cart_class.change_cart(slug, action)
#         return redirect('home')

# Изменить продукты в корзине
def change_cart_view(request, slug, action, id):
    if is_buyer(request.user):
        cart_class = CartAction(request)
        if action == 'add':
            cart_class.add_product(slug, id)
        
        elif action == 'remove':
            cart_class.remove_product(slug, id) 

        return redirect('cart')

# Просмотр корзины
def get_cart_view(request):
    if is_buyer(request.user):
        cart_class = CartAction(request)
        context = cart_class.cart_view()

        return render(request, 'digital_store/cart.html', context)



def get_page_checkout(request):
    user = request.user
    buyer = user.buyer_profile
    order_class = CartAction(request)
    data = order_class.cart_view()
    cart = data['cart']
    if request.method == 'POST':
        data = order_class.checkout_view(request)
        order = data['order']
        ################## bot
        text = f'''
        Пользователь: {user.first_name}
        
        Номер телефона: {user.username}
        
        Номер заказа: #{order.id}
        
        Количесво товаров: {cart.total_quantity}
        
        Цена заказа: {intcomma(order.price)}
        '''

        ################## bot
        order_class.clear_all(request)
        return redirect('success', order_id=order.id)


    context = {
        'buyer': buyer,
        'cart': cart,
    }
    return render(request, 'digital_store/order.html', context)


def success(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user.buyer_profile)
    context = {
        'order': order,
    }
    return render(request, 'digital_store/success.html', context)



# Telegram bot
# def get_order(page):
#     orders = Order.objects.all().order_by('-id')
#     p = []
#     total_order = []
#     for order in orders:
#         p.append(order)
#         if len(p) == 3:
#             total_order.append(p)
#             p = []
#     if p:
#         total_order.append(p)
#
#     paginator = total_order
#     page_obj = paginator[page]
#
#
#     return order_page


########################################################################################################################


# def get_category(request):
#     categories = Category.objects.all().order_by('id')
#     return render(request, 'digital_store/form_list.html', {'categories': categories, 'title': 'title'})


# def delete_category(request, id):
#     category = get_object_or_404(Category, id=id)
#     if request.method == "GET":
#         category.delete()
#     return redirect('category_list')


# def get_category_detail(request, id):
#     if request.method == 'GET':
#         category = Category.objects.get(id=id)
#         return render(request, 'digital_store/category_detail.html', {'category': category})
#     elif request.method == 'POST':
#         category = get_object_or_404(Category, id=id)
#         form = CategoryForm(request.POST, request.FILES, instance=category)
#         if form.is_valid():
#             print(request.FILES)
#             print(form.cleaned_data)
#             form.save()
#         else:
#             print("ERROR:", form.errors)

#         return redirect('category_list')


# def add_category(request):
#     form = CategoryForm(request.POST, request.FILES)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')

#     return render(request, 'digital_store/add_form.html', {
#         'form': form
#     })


# def hello():
#     return render('HELOOOOOOOOOOOOO')

