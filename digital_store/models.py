from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import localtime
from tinymce.models import HTMLField


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категори')
    icon = models.FileField(upload_to='icons/', verbose_name='Иконки', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг категории', null=True, blank=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
        # return reverse('category', kwargs={'slug': self.slug})

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return '-'

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название бренда')
    slug = models.SlugField(unique=True, verbose_name='Слаг бренда', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'



# Профили


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    
    def __str__(self):
        return f'Покупатель: {self.user.first_name} {self.user.last_name}, {self.user.username}' 

    class Meta:
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателей'


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile', verbose_name='Пользователь')
    store_name = models.CharField(max_length=150, verbose_name='Название магазина')
    logo = models.ImageField(upload_to='sellers/logos/', verbose_name='Логотип магазина', blank=True)
    banner = models.ImageField(upload_to='sellers/banners/', verbose_name='Баннер магазина', blank=True)
    description = models.TextField(max_length=500, verbose_name='Описание магазина', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    @property
    def get_logo(self):
            if self.logo:
                return self.logo.url
            else:
                return '-'

    @property
    def get_banner(self):
        if self.banner:
            return self.banner.url
        else:
            return '-'

    # def products.


    def __str__(self):
        return f'Магазин: {self.store_name},  Продавец: {self.user.first_name}'

    class Meta:
        verbose_name = 'Профиль продавца'
        verbose_name_plural = 'Профили продавцов'





class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(unique=True, verbose_name='Слаг товара', null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание товара', blank=True, null=True)
    quantity = models.IntegerField(default=10, verbose_name='Количества товара')
    price = models.IntegerField(default=1000000, verbose_name='Цена товара')
    discount = models.IntegerField(default=0, verbose_name='Скидка на товар')
    color_name = models.CharField(max_length=50, default='Белый', verbose_name='Название цвета')
    color_code = models.CharField(max_length=50, default='#ffffff', verbose_name='Код цвета')
    is_active = models.BooleanField(default=True, verbose_name='Доступно на складе')
    characteristic = HTMLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='brand')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Продавец', related_name='seller_products')


    def discount_price(self):
        if self.discount:
            new_price = int(self.price - (self.price * (self.discount / 100)))
            return new_price

    def installment_price(self):
        new_price = int(self.price / 12)
        return new_price

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return f' Фото товара {self.product.title}'

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фотки товаров'





# Корзина


class Cart(models.Model):
    buyer = models.OneToOneField(BuyerProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')

    @property
    def total_quantity(self):
        total_quantity = 0
        for p in self.productcart_set.all():
            total_quantity += p.quantity
        return total_quantity

    @property
    def total_price(self):
        total_price = 0
        for p in self.productcart_set.all():
            total_price += p.per_total_price
        return total_price


    def __str__(self):
        if self.buyer and self.buyer.user:
            name = self.buyer.user.first_name
        else:
            name = "Unknown"
        return f'Корзина покупателя {name} № {self.id}  '


    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')


    @property
    def per_total_price(self):
        if self.product.discount:
            return self.product.discount_price() * self.quantity
        else:
            return self.product.price * self.quantity



    def __str__(self):
        if self.cart.buyer.user:
            return f'Товар:{self.product.title}, Количество:{self.quantity}, Покупатель: {self.cart.buyer.user}'
        else:
            return f'{self.id}: Unknown'


    class Meta:
        verbose_name = 'Товар в корзине '
        verbose_name_plural = 'Товары корзин'


# Заказы
class Order(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, null=True, blank=True,verbose_name='Покупатель')
    price = models.IntegerField(verbose_name='Цена заказа')
    status = models.CharField(max_length=30, default='Pending')
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True)
    comment = models.TextField(max_length=50, verbose_name='Комментария', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оплаты заказа')



    def __str__(self):
        if self.buyer and self.buyer.user:
            name = self.buyer.user.first_name
        else:
            name = "Unknown"

        return f"Order #{self.id} - {name}"
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



    @property
    def total_quantity(self):
        total_quantity = 0
        for p in self.productcart_set.all():
            total_quantity += p.quantity
        return total_quantity

    @property
    def total_price(self):
        total_price = 0
        for p in self.productcart_set.all():
            total_price += p.per_total_price
        return total_price




class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name="products_order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар',)
    quantity = models.IntegerField(verbose_name='Количества товаров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')


    def __str__(self):
        if self.order and self.order.buyer and self.order.buyer.user.first_name:
            return (
            f'Товар "{self.product.title}" '
            f'Количество: {self.quantity}, '
            f'заказ №: {self.order.id}, '
            f'покупатель {self.order.buyer.user.first_name}'
    )
        else:
            return 'Unknown'


    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказ'

