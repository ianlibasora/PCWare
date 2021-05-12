import json
from django.contrib.sites import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .permissions import *
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


# ------ Product Views ------
def allProducts(request):
    all_p = Product.objects.all()
    httpform = request.GET.get("format", "")
    if httpform == "json":
        serialProducts = serializers.serialize("json", all_p)
        return JsonResponse(serialProducts)
    return render(request, 'all-products.html', {'products': all_p, "Message": None})


def singleProduct(request, prodId):
    prod = get_object_or_404(Product, pk=prodId)
    httpform = request.GET.get("format", "")
    if httpform == "json":
        payload = {
            "product": json.loads(serializers.serialize("json", [prod]))[0],
            "category": json.loads(serializers.serialize("json", [prod.category]))[0]
        }
        return JsonResponse(payload)
    return render(request, 'single-product.html', {'product': prod})


# ------ Product/Category insertion forms (django only) ------
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


# ------ User Management ------
class UserSignUp(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # insert token generator here
        token = Token.objects.create(user=user).save()

        if self.request.GET["format"] == "json":
            return JsonResponse({"Token": token})

        login(self.request, user)
        return redirect("/")

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserSignUp, self).dispatch(request, *args, **kwargs)


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user
    Cart.objects.filter(userID=user).delete()
    logout(request)
    return redirect('/')


# ------ Basket/Checkout Management ------
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def showBasket(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user
    cart = Cart.objects.filter(userID=user).first()

    if cart is None:
        return render(request, 'basket.html', {'Content': False})

    cartItem = CartItem.objects.filter(cartID=cart.cartID)
    if cartItem is None:
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
        return JsonResponse(cartJSON)
    return render(request, 'basket.html', {"cart": cart, 'cartItem': cartItem, "Content": True})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def getCheckout(request):
    user = request.user
    httpform = request.GET.get("format", "")
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user

    if request.method == 'POST':
        if not request.POST:
            bodyUnicode = request.body.decode("utf-8")
            body = json.loads(bodyUnicode)
            address_form = AddressForm(body)
            payment_form = PaymentForm(body)
        else:
            address_form = AddressForm(request.POST)
            payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            addr = address_form.save()
            pay = payment_form.save()

            cart = Cart.objects.filter(userID=user).first()
            cartItems = CartItem.objects.filter(cartID=cart)
            Order(userID=user, addressID=addr, paymentID=pay, total=cart.total).save()
            order = Order.objects.filter(userID=user).last()

            for item in cartItems:
                OrderItem(orderID=order, productID=item.productID, quantity=item.quantity, total=item.total).save()
            cart.delete()

            if httpform == "json":
                return JsonResponse({"orderID": order.orderID})

            orderItems = OrderItem.objects.filter(orderID=order)
            return render(request, 'order-complete.html', {'order': order, "orderItems": orderItems})
    else:
        return render(request, 'checkout.html', {'address_form': AddressForm(), 'payment_form': PaymentForm()})


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


# ------ User Account/Order Info Pages Views ------
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def userHomeView(request):
    if request.user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user
        if user.is_superuser or user.isAdmin:
            return JsonResponse({"username": user.username, "admin": 1})
        return JsonResponse({"username": user.username, "admin": 0})
    return render(request, "account.html")


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def adminViewOrders(request):
    allOrders = Order.objects.all()

    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user
        if not user.is_superuser and not user.isAdmin:
            return HttpResponse(json.dumps({"Response": 0}), content_type="application/json")

        payload = []
        for order in allOrders:
            tmp = {
                "username": order.userID.username,
                "order": json.loads(serializers.serialize("json", [order]))[0]
            }
            payload.append(tmp)
        return JsonResponse({"Response": 1, "orders": payload})
    return render(request, "all-orders.html", {"orders": allOrders})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def adminOrderMoreInfo(request, orderID):
    order = get_object_or_404(Order, pk=orderID)
    orderItems = OrderItem.objects.filter(orderID=order)

    user = request.user
    httpform = request.GET.get("format", "")
    if httpform == "json" and user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user

        if user.isAdmin or user.is_superuser:
            payload = {
                "Response": 1,
                "user": {
                    "firstName": order.userID.first_name,
                    "lastName": order.userID.last_name,
                    "email": order.userID.email,
                    "contact": order.userID.contactNum
                },
                "order": {
                    "orderID": order.orderID,
                    "orderTotal": float(order.total),
                    "date": str(order.date)
                },
                "address": json.loads(serializers.serialize("json", [order.addressID]))[0]
            }
            orderProducts = []
            for item in orderItems:
                tmp = {
                    "quantity": item.quantity,
                    "total": float(item.total),
                    "productID": item.productID.productID,
                    "productName": item.productID.productName,
                    "price": float(item.productID.price)
                }
                orderProducts.append(tmp)
            payload["orderProducts"] = orderProducts
            return JsonResponse(payload)
        return JsonResponse({"Response": 0})
    return render(request, "order-info.html", {"order": order, "orderItems": orderItems})


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
        serialOrders = json.loads(serializers.serialize("json", orders))
        return JsonResponse({"username": user.username, "orders": serialOrders})
    return render(request, "all-orders.html", {"orders": orders})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def myOrderInfo(request, orderID):
    user = request.user
    if user.is_anonymous:
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_object_or_404(Token, key=token).user
    order = get_object_or_404(Order, pk=orderID, userID=user)
    orderItems = OrderItem.objects.filter(orderID=order)

    httpform = request.GET.get("format", "")
    if httpform == "json":
        payload = {
            "user": {
                "firstName": order.userID.first_name,
                "lastName": order.userID.last_name,
                "email": order.userID.email,
                "contact": order.userID.contactNum
            },
            "order": {
                "orderID": order.orderID,
                "orderTotal": float(order.total),
                "date": str(order.date)
            },
            "address": json.loads(serializers.serialize("json", [order.addressID]))[0]
        }
        orderProducts = []
        for item in orderItems:
            tmp = {
                "quantity": item.quantity,
                "total": float(item.total),
                "productID": item.productID.productID,
                "productName": item.productID.productName,
                "price": float(item.productID.price)
            }
            orderProducts.append(tmp)
        payload["orderProducts"] = orderProducts
        return JsonResponse(payload)
    return render(request, "order-info.html", {"order": order, "orderItems": orderItems})


# ------ API Viewsets ------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []
