from django.shortcuts import get_object_or_404

from digital_store.models import Product, ProductCart, Cart, Order, ProductOrder


class CartAddDelete:

    def __init__(self, request):
        self.user = self.user = request.user


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
        cart_price = cart.total_price

        print(products_cart)

        return {
            'products_cart': products_cart,
            'cart': cart,
            'cart_price': cart_price
        }

    def checkout_view(self, request):
        user = request.user
        data = self.cart_view()
        address = request.POST.get('address')
        comment = request.POST.get('comment')

        order = Order.objects.create(user=user, price=data['cart_price'], address=address, comment=comment)

        for p_cart in data['products_cart']:
            ProductOrder.objects.create(order=order, product=p_cart.product, quantity=p_cart.quantity)


        for product_order in order.products_order.all():
            product = product_order.product
            print(product)
            if product_order.quantity <= product.quantity:
                product.quantity -= product_order.quantity

            product.save()

        # print(products)

        return{
            'order': order,
            # 'products_order': products_order,
            'user': user
        }


    def clear_all(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.productcart_set.all().delete()
