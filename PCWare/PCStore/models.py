from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Address(models.Model):
    addressId = models.AutoField(primary_key=True)
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    line3 = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)


class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)
    holderName = models.CharField(max_length=200)
    cardNum = models.IntegerField()
    expireMonth = models.IntegerField()
    expireYear = models.IntegerField()
    cvv = models.IntegerField()


class User(AbstractUser):
    # userId = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contactNum = models.IntegerField()
    isAdmin = models.BooleanField(default=False)
    # addressID = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, default=None, null=True)
    # paymentID = models.OneToOneField(Payment, on_delete=models.CASCADE, blank=True, default=None, null=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "contactNum"]


class ProductCategory(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=100)
    categoryDetails = models.CharField(max_length=200)


class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    productDetails = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.FileField(upload_to='productImg/', blank=True)


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    addressID = models.ForeignKey(Address, on_delete=models.CASCADE)
    paymentID = models.ForeignKey(Payment, on_delete=models.CASCADE)


class OrderItem(models.Model):
    orderItemID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Cart(models.Model):
    cartID = models.AutoField(primary_key=True)
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CartItem(models.Model):
    cartItemID = models.AutoField(primary_key=True)
    cartID = models.ForeignKey(Cart, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
