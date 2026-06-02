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
        users = [
            (20, 'admin2', 'admin212345678', 'Muhammad', 'Mirafzalov', True),
            (21, '+998992222222', 'ziyod12345678', 'Ziyod', 'Avazov', False)
        ]

        for id, username, password, first_name, last_name, is_superuser in users:

            user = User.objects.create(
                id=id, username=username, first_name=first_name,
                last_name=last_name, is_superuser=is_superuser,
                is_staff=is_superuser
            )
            user.set_password(password)
            user.save()

        self.stdout.write(self.style.SUCCESS("Seeding Users completed!"))


    def category_seeder(self):
        categories = [
            (45, 'Кофемашины', 'kofemashiny'),
            (46, 'Смарт-часы', 'smart-chasy')
        ]

        for id, title, slug in categories:

            Category.objects.create(id=id, title=title, slug=slug)

        self.stdout.write(self.style.SUCCESS('Seeding Categories completed'))


    def brand_seeder(self):
        brands = [
            (20, "De'Longhi", 'delonghi'),
            (21, 'HUAWEI', 'huawei')
        ]

        for id, title, slug in brands:
            Brand.objects.create(
                id=id,
                title=title,
                slug=slug
            )

        self.stdout.write(self.style.SUCCESS('Seeding Brands completed'))


    def product_seeder(self):
        products = [
            (20, "Кофемашина De'Longhi ECAM380.95.TB",
             'kofemashina-delonghi-ecam380-95-tb', 30,
             12885500, 0, 'Серебристый', '#C0C0C0', 20, 45),

            (21, "Смарт-часы HUAWEI-Watch FIT 3 Черный",
             'smart-chasy-huawei-watch-fit-3-chernyy', 60,
             1617300, 0, 'Чёрный', '#000000', 21, 46)
        ]

        for id, title, slug, quantity, price, discount, color_name, color_code, brand_id, category_id in products:

            Product.objects.create(
                id=id, title=title, slug=slug, quantity=quantity, price=price,
                discount=discount, color_name=color_name, color_code=color_code,
                brand_id=brand_id, category_id=category_id)

        self.stdout.write(self.style.SUCCESS('Seeding Products completed'))


    def order_seeder(self):
        orders = [(100, 20, 14502800),
                  (101, 21, 12885500),
                  (102, 20, 1617300)]

        for id, user_id, price in orders:
            user = User.objects.get(id=user_id)

            Order.objects.create(id=id, user_id=user.id, price=price)

        self.stdout.write(self.style.SUCCESS("Seeding Orders completed"))