from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
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


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(unique=True, verbose_name='Слаг товара', null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание товара', blank=True, null=True)
    quantity = models.IntegerField(default=10, verbose_name='Количества товара')
    price = models.IntegerField(default=1000000, verbose_name='Цена товара')
    color_name = models.CharField(max_length=50, default='Белый', verbose_name='Название цвета')
    color_code = models.CharField(max_length=50, default='#ffffff', verbose_name='Код цвета')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение', null=True, blank=True)
    discount = models.IntegerField(default=0, verbose_name='Скидка на товар')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='brand')
    is_active = models.BooleanField(default=True)
    characteristic = HTMLField(blank=True)


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
        return self.title

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фотки товаров'



class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', verbose_name='Фото профиля', blank=True)
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name='Дата добавление')


    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://i.pinimg.com/originals/5f/91/41/5f91413c8a9e766a5139c6cfe5caa837.jpg'




    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'



# Корзина


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
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
        return f'Корзина покупателя № {self.user}'

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
        return f'Товар:{self.product.title}, Количество:{self.quantity}'

    class Meta:
        verbose_name = 'Товар в корзине '
        verbose_name_plural = 'Товары корзин'



class Delivery(models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес')
    comment = models.TextField(max_length=50, verbose_name='Комментария', blank=True, null=True)


    def __str__(self):
       return f'Адрес: {self.address}'


    class Meta:
        verbose_name = 'Доставка заказа'
        verbose_name_plural = 'Доставки заказ'



# Заказы
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    price = models.IntegerField(verbose_name='Цена заказа')
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, verbose_name='Доставка')
    status = models.CharField(max_length=30, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оплаты заказа')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количества товаров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')


    def __str__(self):
        return f'Товар {self.product.title}, заказа №: {self.order.id}, покупателя {self.order.user.username}'


    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказ'

