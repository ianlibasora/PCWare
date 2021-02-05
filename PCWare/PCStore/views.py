from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def all_products(request):
    all_p = Product.objects.all()
    return render(request, 'all_products.html', {'products': all_p})