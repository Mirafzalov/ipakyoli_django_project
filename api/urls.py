from django.urls import path
from .views import *

urlpatterns = [
    path("api/v1/categories/", category_list_veiw),
    path("api/v1/products/", product_list_view),
    path("api/v1/products/<int:pk>", get_products_by_category),
]