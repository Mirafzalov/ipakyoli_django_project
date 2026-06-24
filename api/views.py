from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from digital_store.models import *
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, BrandSerializer

# Create your views here.


# Category View



class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


# Brand View
class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Product Views

class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    
    

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    

    # def put(self, request, id):
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product, request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # def patch(self, request, id):
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product, request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)




# Order View

class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
    




# Rgister API view

class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'buyer')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'User with this name already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)

        if role == 'seller':
            SellerProfile.objects.create(user=user, store_name=f"{username}'s store")

        elif role == 'buyer':
            BuyerProfile.objects.create(user=user)  

        else:
            return Response(
                {'error': 'Invalid role'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'message': 'User is created'},
            status=status.HTTP_201_CREATED
        )    
        return Response({'meassage': 'User is created'}, status=status.HTTP_201_CREATED)

            
            
        

# Seller Views

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user, 'seller_profile'))

class SellerProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller_profile)
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_profile)














##############################################

# @api_view(['GET', 'POST'])
# def category_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# @api_view()
# def product_list_view(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)



# @api_view()
# def get_products_by_category(request, pk):
#     products = Product.objects.filter(category=pk)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)