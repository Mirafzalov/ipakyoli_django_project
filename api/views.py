from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from digital_store.models import *
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def category_list_veiw(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view()
def product_list_view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view()
def get_products_by_category(request, pk):
    products = Product.objects.filter(category=pk)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)