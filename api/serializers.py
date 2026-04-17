from digital_store.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')




class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    color_name = serializers.CharField()


