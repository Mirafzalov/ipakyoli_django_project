from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from digital_store.models import *
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, BrandSerializer, CartSerializer, ProductCartSerializer

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

            
            
        


# Permissions

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user, 'seller_profile'))


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.seller == request.user.seller_profile



class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user, 'buyer_profile'))
        


class IsOnlyOwner(BasePermission):
    def has_object_permission(self, request, viewe, obj):
        return obj.buyer == request.user.buyer_profile


# Seller Views
class SellerProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller_profile)

    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_profile)


class SellerProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSeller, IsOwnerOrReadOnly]
    lookup_field = 'id'
    
    


# Cart
class CartView(APIView):
    permission_classes = [IsBuyer]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(buyer=request.user.buyer_profile)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    

class ProductCartupdateView(ListCreateAPIView):
    serializer_class = ProductCartSerializer
    permission_classes = [IsBuyer]
    
    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(buyer=self.request.user.buyer_profile)
        return ProductCart.objects.filter(cart=cart)
    
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(buyer=self.request.user.buyer_profile)
        serializer.save(cart=cart)
    
    
    
    

# Order View

class MyOrdersListView(ListAPIView):
    permission_classes = [IsBuyer]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user.buyer_profile)
    


class PlaceOrderView(APIView):
    permission_classes = [IsBuyer]
    def post(self, request):
        cart = Cart.objects.get(buyer=request.user.buyer_profile)
        cart_price = cart.total_price
        
        if not  ProductCart.objects.filter(cart=cart).exists():
            return Response({'error': 'Your cart is empty, add some products to the cart in order to place order'}, status=status.HTTP_400_BAD_REQUEST)
        
        products_cart = ProductCart.objects.filter(cart=cart)
        
        
        for p_cart in products_cart:
            if p_cart.quantity > p_cart.product.quantity:
                return Response({'error': 'Out of the stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        with transaction.atomic(): 
            
            order = Order.objects.create(buyer=request.user.buyer_profile, price=cart_price)
            
            for p_order in products_cart:
                ProductOrder.objects.create(order=order, product=p_order.product, quantity=p_order.quantity)
                
                product = p_cart.product
                
                Product.objects.filter(id=product.id).update(quantity=F('quantity') - p_cart.quantity)
                        
        serializer = OrderSerializer(order)
        products_cart.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        
        
        
              
  









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