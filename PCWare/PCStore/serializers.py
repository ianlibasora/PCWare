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


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contactNum', 'password']

        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            contactNum=self.validated_data['contactNum'],
            password=self.validated_data['password']
        )
        user.set_password(password)
        user.save()
        return user
