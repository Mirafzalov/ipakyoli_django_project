from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from humanize import intcomma

from digital_store.models import Product, ProductCart, Cart, Order, ProductOrder


class CartAddDelete:

    def __init__(self, request):
        self.user = request.user


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
        data = self.cart_view()
        address = request.POST.get('address')
        comment = request.POST.get('comment')

        order = Order.objects.create(user=self.user, price=data['cart_price'], address=address, comment=comment)

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
            'user': self.user
        }


    def clear_all(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.productcart_set.all().delete()




# def get_order_history():
#     # orders = Order.objects.all().order_by('-created_at')[:10]
#     orders = Order.objects.all().order_by('-created_at')[:10]
#     text = []
#     for order in orders:
#         text.append(f'''
#         Пользователь: {order.user.first_name}
#
#         Номер телефона: {order.user.username}
#
#         Номер заказа: #{order.id}
#
#         Цена заказа: {intcomma(order.price)}
#         --------------------------------------------------------------
#         Заказ создан:  {(order.created_at).strftime("%d.%m.%Y %H:%M")}
#         ''')
#
#     print(f'''
# #######################
# {text}
# ####################''')
#     print(text)
#     return text


def get_history(request):
    orders = Order.objects.all()[:10]

    data = []

    for order in orders:
        data.append({
            'user': order.user.first_name,
            'phone': order.user.username,
            'order_id': order.id,
            'price': order.price,
            'created_at': order.created_at
        })
    print(data)
    return JsonResponse(data, safe=False)

