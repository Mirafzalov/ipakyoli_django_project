from django.urls import path
from .views import *


from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

  

urlpatterns = [
    path("auth/register/", RegisterApiView.as_view(), name='api_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    
    path("categories/", CategoryListView.as_view()),
    path("brands/", BrandListView.as_view()),
    path("products/", ProductListView.as_view()),
    path("product/<int:id>/", ProductDetailView.as_view()),
    path("orders/", OrderListView.as_view()),
    
    path('seller/products/', SellerProductListCreateView.as_view())
    

    
]

