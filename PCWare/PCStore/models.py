from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=100)
    categoryDetails = models.CharField(max_length=200)


class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    productDetails = models.CharField(max_length=200)
    categoryID = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


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
    addressId = models.ForeignKey(Address, on_delete=models.CASCADE)


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contactNum = models.IntegerField()
    addressId = models.ForeignKey(Address, on_delete=models.CASCADE)
    paymentId = models.ForeignKey(Payment, on_delete=models.CASCADE)

