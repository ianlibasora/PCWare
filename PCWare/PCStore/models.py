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
