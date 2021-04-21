import json

from django.contrib.sites import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

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
    httpform = request.GET.get("format", "")
    if httpform == "json":
        serialProducts = serializers.serialize("json", all_p)
        return HttpResponse(serialProducts, content_type="application/json")
    return render(request, 'all-products.html', {'products': all_p, "Message": None})


def singleProduct(request, prodId):
    prod = get_object_or_404(Product, pk=prodId)
    httpform = request.GET.get("format", "")
    if httpform == "json":
        payload = {
            "product": json.loads(serializers.serialize("json", [prod]))[0],
            "category": json.loads(serializers.serialize("json", [prod.category]))[0]
        }
        return HttpResponse(json.dumps(payload), content_type="application/json")
    return render(request, 'single-product.html', {'product': prod})


@login_required
@admin_required
def productCategoryForm(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)

        if form.is_valid():
            new_product = form.save()
            return redirect("/account")
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


@api_view(['POST',])
def RegistrationView(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user."
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors

    return Response(data)


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    Cart.objects.filter(userID=request.user).delete()
    logout(request)
    return redirect('/')


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def addCart(request, productID):
    user = request.user
    all_p = Product.objects.all()
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user

    cart = Cart.objects.filter(userID=user).first()
    if cart is None:
        Cart(userID=user).save()
        cart = Cart.objects.filter(userID=user).first()

    item = get_object_or_404(Product, pk=productID)
    cartItem = CartItem.objects.filter(cartID=cart, productID=item.productID).first()
    if cartItem is None:
        CartItem(cartID=cart, productID=item, total=item.price).save()
        cart.total += item.price
    else:
        cartItem.quantity += 1
        cartItem.total += item.price
        cart.total += item.price
        cartItem.save()
    cart.save()

    return render(request, 'all-products.html', {'products': all_p, "Message": f"Added {item.productName} to cart."})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def removeCart(request, productID):
    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user

    cart = get_object_or_404(Cart, userID=user)
    product = get_object_or_404(Product, pk=productID)
    cartItem = get_object_or_404(CartItem, cartID=cart, productID=productID)

    cartItem.quantity -= 1
    cartItem.total -= cartItem.productID.price
    cart.total -= cartItem.productID.price

    cartItem.delete() if cartItem.quantity == 0 else cartItem.save()
    cart.delete() if len(CartItem.objects.filter(cartID=cart)) == 0 else cart.save()
    
    allP = Product.objects.all()
    return render(request, "all-products.html", {"products": allP, "Message": f"Removed {product.productName} from cart."})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def showBasket(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user
    cart = Cart.objects.filter(userID=user).first()

    if cart is None:
        # Handle 404 in frontend
        return render(request, 'basket.html', {'Content': False})

    cartItem = CartItem.objects.filter(cartID=cart.cartID)
    if cartItem is None:
        # Handle 404 in frontend
        return render(request, 'basket.html', {'Content': False})

    httpform = request.GET.get("format", "")
    if httpform == "json":
        cartJSON = {
            "total": float(cart.total)
        }
        cartItemJSON = []
        for item in cartItem:
            tmp = {
                "quantity": item.quantity,
                "total": float(item.total),
                "product": json.loads(serializers.serialize("json", [item.productID]))[0],
                "category": json.loads(serializers.serialize("json", [item.productID.category]))[0]
            }
            cartItemJSON.append(tmp)

        cartJSON["cartitems"] = cartItemJSON
        return HttpResponse(json.dumps(cartJSON), content_type="application/json")
    return render(request, 'basket.html', {"cart": cart, 'cartItem': cartItem, "Content": True})

@login_required
def getCheckout(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            addr = address_form.save()
            pay = payment_form.save()

            cart = Cart.objects.filter(userID=request.user).first()
            cartItems = CartItem.objects.filter(cartID=cart)
            Order(userID=request.user, addressID=addr, paymentID=pay, total=cart.total).save()
            order = Order.objects.filter(userID=request.user).last()

            for item in cartItems:
                OrderItem(orderID=order, productID=item.productID, quantity=item.quantity, total=item.total).save()
            cart.delete()

            orderItems = OrderItem.objects.filter(orderID=order)
            return render(request, 'order-complete.html', {'order': order, "orderItems": orderItems})
    else:
        return render(request, 'checkout.html', {'address_form': AddressForm(), 'payment_form': PaymentForm()})


@login_required
@admin_required
def adminViewOrders(request):
    allOrders = Order.objects.all()
    httpform = request.GET.get("format", "")
    if httpform == "json":
        serialOrders = serializers.serialize("json", allOrders)
        return HttpResponse(serialOrders, content_type="application/json")
    return render(request, "all-orders.html", {"orders": allOrders})


@login_required
@admin_required
def adminOrderMoreInfo(request, orderID):
    order = get_object_or_404(Order, pk=orderID)
    orderItems = OrderItem.objects.filter(orderID=order)
    return render(request, "order-info.html", {"order": order, "orderItems": orderItems})


@login_required
def userHomeView(request):
    return render(request, "account.html")


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def myOrders(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user

    orders = Order.objects.filter(userID=user)
    httpform = request.GET.get("format", "")
    if httpform == "json":
        serialOrders = serializers.serialize("json", orders)
        return HttpResponse(serialOrders, content_type="application/json")

    return render(request, "all-orders.html", {"orders": orders})


@login_required
def myOrderInfo(request, orderID):
    order = get_object_or_404(Order, pk=orderID, userID=request.user)
    orderItems = OrderItem.objects.filter(orderID=order)
    return render(request, "order-info.html", {"order": order, "orderItems": orderItems})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []
    permission_classes = []

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
