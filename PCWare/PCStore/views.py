from django.contrib.sites import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView
from rest_framework import viewsets
from .serializers import *
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .permissions import *
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import HttpResponse


# Create your views here.


def index(request):
    return render(request, "index.html")


def allProducts(request):
    all_p = Product.objects.all()
    format = requests.GET.get("format", "")
    if format == "json":
        serialProducts = serializers.serialize("json", all_p)
        return HttpResponse(serialProducts, content_type="application/json")
    return render(request, 'all-products.html', {'products': all_p, "Message": False})


def singleProduct(request, prodId):
    prod = get_object_or_404(Product, pk=prodId)
    return render(request, 'single-product.html', {'product': prod})


@login_required
@admin_required
def productCategoryForm(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)

        if form.is_valid():
            new_product = form.save()
            return redirect("/")
    else:
        form = ProductCategoryForm()
        return render(request, 'category-form.html', {'form': form})


@login_required
@admin_required
def productForm(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            new_product = form.save()
            return render(request, 'single-product.html', {'product': new_product})

    else:
        form = ProductForm()
        return render(request, 'product-form.html', {'form': form})


class UserSignUp(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    Cart.objects.filter(userID=request.user).delete()
    logout(request)
    return redirect('/')


@login_required
def addCart(request, productID):
    user = request.user
    all_p = Product.objects.all()

    cart = Cart.objects.filter(userID=user).first()
    if cart is None:
        Cart(userID=user).save()
        cart = Cart.objects.filter(userID=user).first()

    item = get_object_or_404(Product, pk=productID)
    if item is None:
        return render(request, 'all-products.html', {'products': all_p, "Message": "Warning. Invalid operation"})

    cartItem = CartItem.objects.filter(cartID=cart, productID=item.productID).first()
    if cartItem is None:
        CartItem(cartID=cart, productID=item).save()
        cartItem = CartItem.objects.filter(cartID=cart, productID=item).first()
    else:
        cartItem.quantity += 1
        cartItem.save()

    return render(request, 'all-products.html', {'products': all_p, "Message": f"Added {item.productName} to caer"})


@login_required
def showBasket(request):
    user = request.user
    cart = Cart.objects.filter(userID=user).first()

    if cart is None:
        return render(request, 'basket.html', {'Content': False})

    cartItem = CartItem.objects.filter(cartID=cart.cartID)
    return render(request, 'basket.html', {'cart': cartItem, "Content": True})


@login_required
def getCheckout(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            addr = address_form.save()
            pay = payment_form.save()

            Order(userID=request.user, addressID=addr, paymentID=pay).save()
            order = Order.objects.filter(userID=request.user).last()
            cart = Cart.objects.filter(userID=request.user).first()
            cartItems = CartItem.objects.filter(cartID=cart)

            # Copy cartItem objects into orderItem objects
            for item in cartItems:
                OrderItem(orderID=order, productID=item.productID, quantity=item.quantity).save()
                order.total += (item.productID.price * item.quantity)
            order.save()

            # Delete user's `cart`
            # Note: `cart` deletion cascades to `cartItem`
            cart.delete()
            orderItems = OrderItem.objects.filter(orderID=order)
            return render(request, 'order-complete.html', {'order': order, "orderItems": orderItems})
    else:
        content = {
            'address_form': AddressForm(),
            'payment_form': PaymentForm()
        }
    return render(request, 'checkout.html', content)


@login_required
@admin_required
def viewOrders(request):
    allOrders = Order.objects.all()
    return render(request, "all-orders.html", {"orders": allOrders})


@login_required
@admin_required
def orderMoreInfo(request, orderID):
    order = get_object_or_404(Order, pk=orderID)
    orderItems = OrderItem.objects.filter(orderID=order)
    return render(request, "order-info.html", {"order": order, "orderItems": orderItems})


@login_required
@admin_required
def adminHomeView(request):
    return render(request, "admin-home.html")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
