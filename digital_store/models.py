from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категори')
    icon = models.FileField(upload_to='icons/', verbose_name='Иконки', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг категории', blank=True)

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
    slug = models.SlugField(unique=True, verbose_name='Слаг бренда', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(unique=True, verbose_name='Слаг товара', blank=True)
    description = models.CharField(max_length=300, verbose_name='Описание товара')
    quantity = models.IntegerField(default=10, verbose_name='Количества товара')
    price = models.IntegerField(default=1000000, verbose_name='Цена товара')
    color_name = models.CharField(max_length=50, default='Белый', verbose_name='Название цвета')
    color_code = models.CharField(max_length=50, default='#ffffff', verbose_name='Код цвета')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение', null=True, blank=True)
    discount = models.IntegerField(default=0, verbose_name='Скидка на товар')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='brand')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец')
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# Write the Order model — fields: buyer (FK to User), product (FK to Product),
# quantity, status (choices: pending / confirmed / cancelled), created
#
# Add __str__ to all three models
#
# Run python manage.py makemigrations — creates the migration file
#
# Run python manage.py migrate — creates the actual tables in SQLite
# Check: Open the Django shell and create one Category and one Product manually.



class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=10, verbose_name='Количества товара')
    status = models.CharField(max_length=30, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
