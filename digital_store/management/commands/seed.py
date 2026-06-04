from django.contrib.auth.models import User
from django.core.management import BaseCommand

from digital_store.models import Category, Product, Brand, Order


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.user_seeder()
        self.category_seeder()
        self.brand_seeder()
        self.product_seeder()
        self.order_seeder()

        self.stdout.write(self.style.SUCCESS("Seeding ALL completed!"))


    def user_seeder(self):

        if not User.objects.filter(username='admin2').exists():
            user = User.objects.create_superuser(username='admin2',
            password='admin212345678',# Better put password in .env file to keep it private
            first_name='Muhammad',
            last_name='Mirafzalov')


        user, created = User.objects.get_or_create(username='+998992222222',
                                   defaults=dict(
                                       first_name='Ziyod',
                                       last_name='Avazov')
                                          )
        if created:
            user.set_password('ziyod12345678')
            user.save()



        self.stdout.write(self.style.SUCCESS("Seeding Users completed!"))


    def category_seeder(self):
        categories = [
            ('Кофемашины', 'kofemashiny'),
            ('Смарт-часы', 'smart-chasy')
        ]

        for title, slug in categories:
            Category.objects.get_or_create(title=title, slug=slug)

        self.stdout.write(self.style.SUCCESS('Seeding Categories completed'))


    def brand_seeder(self):
        brands = [
            ("De'Longhi", 'delonghi'),
            ('HUAWEI', 'huawei')
        ]

        for title, slug in brands:
            Brand.objects.get_or_create(
                title=title,
                slug=slug
            )

        self.stdout.write(self.style.SUCCESS('Seeding Brands completed'))


    def product_seeder(self):

        kofemashiny_id = Category.objects.get(title="Кофемашины").id
        smart_chasy_id = Category.objects.get(title="Смарт-часы").id

        delonghi_id = Brand.objects.get(title="De'Longhi").id
        huawei_id = Brand.objects.get(title="HUAWEI").id

        products = [
        {
            'title': "Кофемашина De'Longhi ECAM380.95.TB",
            'slug': 'kofemashina-delonghi-ecam380-95-tb',
            'quantity': 30,
            'price': 12885500,
            'discount': 0,
            'color_name': 'Серебристый',
            'color_code': '#C0C0C0',
            'category_id': kofemashiny_id,
            'brand_id': delonghi_id
            },
        {
            'title': "Смарт-часы HUAWEI-Watch FIT 3 Черный",
             'slug': 'smart-chasy-huawei-watch-fit-3-chernyy',
            'quantity': 60,
             'price': 1617300,
            'discount': 0,
            'color_name': 'Чёрный',
            'color_code': '#000000',
            'category_id': smart_chasy_id,
            'brand_id': huawei_id
             }
        ]

        for data in products:
            title = data.pop('title')
            Product.objects.get_or_create(
                title=title,
                defaults=data
            )

        self.stdout.write(self.style.SUCCESS('Seeding Products completed'))

    def order_seeder(self):
        super_user = User.objects.get(username='admin2')
        user = User.objects.get(username='+998992222222')

        coffee_machine = Product.objects.get(
            title="Кофемашина De'Longhi ECAM380.95.TB"
        )

        smartwatch = Product.objects.get(
            title='Смарт-часы HUAWEI-Watch FIT 3 Черный'
        )

        orders = [
            (super_user.id, coffee_machine.price + smartwatch.price),
            (super_user.id, coffee_machine.price),
            (user.id, smartwatch.price),
        ]

        for user_id, price in orders:
            Order.objects.create(user_id=user_id, price=price)


        self.stdout.write(
            self.style.SUCCESS("Seeding Orders completed")
        )