from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def allProducts(request):
    all_p = Product.objects.all()
    return render(request, 'all_products.html', {'products': all_p})

def singleProduct(request, prodId):
    prod = get_object_or_404(Product, pk=prodId)
    return render(request, 'single_product.html', {'product': prod})

