from .views import *
from django.urls import path

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='detail'),

    path('category_list/', get_category, name='category_list'),
    path('category_list/<id>', get_category_detail, name='category_detail'),
    path('delete_category/<id>', delete_category, name='delete_category'),
    path('add_category/', add_category, name='add_category'),
]