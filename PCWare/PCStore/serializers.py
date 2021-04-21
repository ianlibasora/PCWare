from django.urls import path, include
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="categoryName")

    class Meta:
        model = Product
        fields = ["productID", "productName", "productDetails", "category", "stock", "price", "picture"]

class OrderSerializer(serializers.ModelSerializer):
    userID = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Order
        fields = ["orderID", "userID", "total", "date"]