from django.http import JsonResponse
from humanize import intcomma
from django.shortcuts import render, get_object_or_404, redirect
from digital_store.models import Product, ProductCart, Cart, Order, ProductOrder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
        product_cart, created = ProductCart.objects.get_object_or_create(product=product, cart=cart)

        if not created:
            if product.quantity > 0 and product_cart.quantity < product.quantity:
                product_cart.quantity += 1
                product_cart.save()
        
        
    # Убарть Товар с корзины        
    def remove_product_cart(self):
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
        
        
        
            
            
        
    # def change_cart(self, slug, action, id):

    #     product = Product.objects.get(slug=slug, id=id)

    #     cart, created = Cart.objects.get_or_create(buyer=self.buyer)
    #     print('It worked')

    #     product_cart, product_created = ProductCart.objects.get_or_create(cart=cart, product=product)

    #     if product_created == False:
    #         if action == 'add' and product.quantity > 0 and product_cart.quantity < product.quantity:
    #             product_cart.quantity += 1
    #         elif action == 'delete':
    #             product_cart.quantity -= 1

    #         elif action == 'clear':
    #             product_cart.quantity = 0

    #         product_cart.save()

    #         if product_cart.quantity <= 0:
    #             product_cart.delete()


    @login_required
    @require_POST
    def checkout_view(self, request):
        data = self.cart_view()
        address = request.POST.get('address')
        comment = request.POST.get('comment')

        order = Order.objects.create(buyer=self.buyer, price=data['cart_price'], address=address, comment=comment)

        for p_cart in data['products_cart']:
            ProductOrder.objects.create(order=order, product=p_cart.product, quantity=p_cart.quantity)


        for product_order in order.products_order.all():
            product = product_order.product
            print(product)
            if product_order.quantity <= product.quantity:
                product.quantity -= product_order.quantity

            product.save()


        return{
            'order': order,
            'buyer': self.buyer
        }


    def clear_all(self, request):
        cart = Cart.objects.get(buyer=self.buyer)
        cart.productcart_set.all().delete()

