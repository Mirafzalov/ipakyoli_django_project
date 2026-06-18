from .tests import get_order
from .views import *
from django.urls import path

urlpatterns = [
    # path('', MainPage.as_view(), name='main'),
    path('', product_list_view, name='home'),
    path('product/<slug:slug>-<int:id>/', product_detail_view, name='product_detail'),
    path('products/', product_filter_view, name='filter_products'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_user_view, name='profile'),
    path('seller_profile/<int:id>/', seller_profile, name='seller_profile'),
    
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller_dashboard/add_product/', add_product, name='add_product'),
    path('seller_dashboard/edit_product/<int:id>/', edit_product, name='edit_product'),
    path('seller_dashboard/delete_product/<int:id>/', delete_product, name='delete_product'),
    
    
    path('settings/', edit_password_view, name='settings'),
    path('add_cart/<slug:slug>/<str:action>/',  add_cart_view, name='add_cart'),
    
    path('cart/', get_cart_view, name='cart'),
    
    path('cart/<str:action>/<slug:slug>/<int:id>/', change_cart_view, name='change_cart'),
    
    path('order/', get_page_checkout, name='order'),
    path('order/success/<int:order_id>/', success, name='success'),
    # path('cart/delete/<slug:slug>/', cart_product_delete, name='cart_delete'),

    # Telegram
    path('api/orders/history/', get_order)

    # path('product/<slug:slug>/', ProductDetail.as_view(), name='detail'),

#     path('category_list/', get_category, name='category_list'),
#     path('category_list/<id>', get_category_detail, name='category_detail'),
#     path('delete_category/<id>', delete_category, name='delete_category'),
#     path('add_category/', add_category, name='add_category'),
#     path('register/', register_view, name='reg_form'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout, name='logout'),
]