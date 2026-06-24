from digital_store.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        exclude = ['logo', 'banner', 'description']

        
        
class BuyerProfileserializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'
               

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Product
        exclude = ('characteristic',)
        
        
        
        
class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)
    
    total_quantity = serializers.SerializerMethodField()
    
    def get_total_quantity(self, obj):
        products_order = ProductOrder.objects.filter(order=obj)
        total_quantity = 0
        for product in products_order:
            total_quantity += product.quantity
        return total_quantity




    class Meta:
        model = Order
        fields = ['id', 'buyer', 'price', 'status', 'total_quantity' ]
        