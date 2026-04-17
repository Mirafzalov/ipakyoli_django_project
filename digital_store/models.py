from django.db import models
from django.urls import reverse


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
    quantity = models.IntegerField(default=10, verbose_name='Количества товара')
    price = models.IntegerField(default=1000000, verbose_name='Цена товара')
    color_name = models.CharField(max_length=50, default='Белый', verbose_name='Название цвета')
    color_code = models.CharField(max_length=50, default='#ffffff', verbose_name='Код цвета', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение', null=True, blank=True)
    discount = models.IntegerField(default=0, verbose_name='Скидка на товар')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='brand')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})


    def first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return ''
        else:
            return ''

    def divided_price(self):
        if self.discount:
            self.price = int(self.price * (1 - (self.discount / 100)))
        return self.price // 12


    def get_price(self):
        if self.discount:
            return int(self.price * (1 - (self.discount / 100)))
        else:
            return int(self.price)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
