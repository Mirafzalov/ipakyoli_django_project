from django.shortcuts import get_object_or_404

from digital_store.models import Product, ProductCart, Cart


class CartAddDelete:

    def __init__(self, request):
        self.user = self.user = request.user

    # def add_cart_product(self, slug):
    #     product = Product.objects.get(slug=slug)
    #     cart, created = Cart.objects.get_or_create(user=self.user)
    #     product_cart, product_created = ProductCart.objects.get_or_create(cart=cart, product=product)
    #

    def change_cart(self, slug, action):

        product = Product.objects.get(slug=slug)

        cart, created = Cart.objects.get_or_create(user=self.user)
        product_cart, product_created = ProductCart.objects.get_or_create(cart=cart, product=product)


        if product_created == False:
            if action == 'add' and product.quantity > 0 and product_cart.quantity < product.quantity:
                product_cart.quantity += 1
            elif action == 'delete':
                product_cart.quantity -= 1

            elif action == 'clear':
                product_cart.quantity = 0

            product_cart.save()

            if product_cart.quantity <= 0:
                product_cart.delete()



    # Просмотр корзины
    def cart_view(self):
        cart = get_object_or_404(Cart, user=self.user)
        products_cart = cart.productcart_set.all()

        print(products_cart)

        return {
        'products_cart': products_cart,
        'cart': cart
    }