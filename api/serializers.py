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
    # category = serializers.StringRelatedField(read_only=True)
    # brand = serializers.StringRelatedField(read_only=True)
    # seller = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Product
        exclude = ('characteristic',)
        
        


# Cart Serializer


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = '__all__'
        read_only_fields = ['cart']

        

class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    
    def get_products(self, obj):
        products = ProductCart.objects.filter(cart=obj)
        return ProductCartSerializer(products, many=True).data
    
    class Meta:
        model = Cart
        fields = ['id', 'buyer', 'created_at', 'products']
        
        

  
  
# Order Serializer
        
class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_products = serializers.SerializerMethodField()
    
    
    def get_products(self, obj):
        products = ProductOrder.objects.filter(order=obj)
        return ProductOrderSerializer(products, many=True).data
        
        
    def get_total_products(self, obj):
        products_order = ProductOrder.objects.filter(order=obj)
        total_products = 0
        for product in products_order:
            total_products += product.quantity
        return total_products



    class Meta:
        model = Order
        fields = ['id', 'buyer', 'price', 'status', 'total_products', 'products' ]
        