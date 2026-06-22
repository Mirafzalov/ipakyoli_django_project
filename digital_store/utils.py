from django.http import JsonResponse
from humanize import intcomma
from django.shortcuts import render, get_object_or_404, redirect
from digital_store.models import Product, ProductCart, Cart, Order, ProductOrder
from django.contrib.auth.decorators import login_required
from digital_store.templatetags.user_roles import  is_buyer 
from django.contrib import messages
from django.db.models import F

from django.db import transaction

class CartAction:


    def __init__(self, request):
        self.user = request.user
        self.buyer = self.user.buyer_profile

    def get_or_create_cart(self):
        cart, created = Cart.objects.get_or_create(buyer=self.buyer)
        return cart
    
    #Добавить Товар в корзину
    def add_product_cart(self, slug, id):
        try:
            product = Product.objects.get(slug=slug, id=id)
            
        except Product.DoesNotExist:
            return {'error': 'Такого товара нету'}
        
        
        if product.quantity <= 0:
            return {'error': 'Товара нет в наличии'}
        
        cart = self.get_or_create_cart()
        product_cart, created = ProductCart.objects.get_or_create(product=product, cart=cart)
    
        if not created:
            if product.quantity > 0 and product_cart.quantity < product.quantity:
                product_cart.quantity += 1
                product_cart.save()
        
        
    # Убарть Товар с корзины        
    def remove_product_cart(self, slug, id):
        try:
            product = Product.objects.get(slug=slug, id=id)
            
        except Product.DoesNotExist:
            return {'error': 'Такого товара нету'}
        
        
        if product.quantity <= 0:
            return {'error': 'Товара нет в наличии'}
        
        cart = self.get_or_create_cart()
        product_cart = get_object_or_404(ProductCart, product=product, cart=cart)

        if product_cart.quantity > 0:
            product_cart.quantity -= 1
            product_cart.save()
        
        if product_cart.quantity <= 0:
            product_cart.delete()
            
    
    def cart_view(self):
        cart = self.get_or_create_cart()
        products_cart = ProductCart.objects.filter(cart=cart)
        cart_price = cart.total_price
        
        return {
            'products_cart': products_cart,
            'cart': cart,
            'cart_price': cart_price
        }
        
        
    def clear_all(self, slug, id):
        cart = self.get_or_create_cart()
        product = Product.objects.get(slug=slug, id=id)
        products_cart = ProductCart.objects.filter(cart=cart, product=product)
        products_cart.delete()
            
            
        

class OrderAction:
    def __init__(self, request):
        self.user = request.user
        self.buyer = self.user.buyer_profile


    def place_order(self, request):
        if self.buyer:
            if request.method == 'POST':
                data = CartAction(request).cart_view()
                address = request.POST.get('address')
                comment = request.POST.get('comment')
                
                for p_cart in data['products_cart']:
                    if p_cart.quantity > p_cart.product.quantity:
                        messages.error(request, "Недостаточно товара в наличии.")
                        return redirect('cart')
                        
                with transaction.atomic(): 
                    
                    order = Order.objects.create(buyer=self.buyer, price=data['cart_price'], address=address, comment=comment)

                    for p_cart in data['products_cart']:
                        ProductOrder.objects.create(order=order, product=p_cart.product, quantity=p_cart.quantity)

                        product = p_cart.product
                        
                        Product.objects.filter(id=product.id, slug=product.slug).update(quantity=F('quantity') - p_cart.quantity)
                        


                    return order