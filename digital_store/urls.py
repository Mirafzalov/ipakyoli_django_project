from .views import *
from django.urls import path

urlpatterns = [
    # path('', MainPage.as_view(), name='main'),
    path('home/', product_list_view, name='products'),
    path('product/<slug:slug>-<int:id>/', product_detail_view, name='product_detail'),
    path('products/', product_filter_view, name='filter_products'),

    # path('product/<slug:slug>/', ProductDetail.as_view(), name='detail'),

    path('category_list/', get_category, name='category_list'),
    path('category_list/<id>', get_category_detail, name='category_detail'),
    path('delete_category/<id>', delete_category, name='delete_category'),
    path('add_category/', add_category, name='add_category'),
    path('register/', register_view, name='reg_form'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout'),
]