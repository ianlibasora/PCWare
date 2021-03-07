from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .permissions import *
from django.contrib.auth.views import LoginView


# Create your views here.

def index(request):
    return render(request, "index.html")


def allProducts(request):
    all_p = Product.objects.all()
    return render(request, 'all-products.html', {'products': all_p})


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
    logout(request)
    return redirect('/')


@login_required
def addCart(request, productID):
    user = request.user
    cart = Cart.objects.filter(userID=user).first()
    if cart is None:
        Cart(userID=user).save()
        cart = Cart.objects.filter(userID=user).first()
    item = get_object_or_404(Product, pk=productID)
    cartItem = CartItem.objects.filter(cartID=cart, productID=item.productID).first()

    if cartItem is None:
        CartItem(cartID=cart, productID=item).save()
        cartItem = CartItem.objects.filter(cartID=cart, productID=item).first()
    else:
        cartItem.quantity += 1
        cartItem.save()

    return redirect("/all-products")


@login_required
def showBasket(request):
    user = request.user
    cart = Cart.objects.filter(userID=user).first()

    if not cart:
        cart = Cart(userID=user).save()

    cartItem = CartItem.objects.filter(cartID=cart.cartID)

    return render(request, 'basket.html', {'cart': cartItem})


@login_required
def getCheckout(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            addr = address_form.save()
            pay = payment_form.save()

            Order(userID=request.user, addressID=addr, paymentID=pay).save()
            order = Order.objects.filter(userID=request.user).first()
            cart = Cart.objects.filter(userID=request.user).first()
            cartItems = CartItem.objects.filter(cartID=cart)
            total = 0

            # Copy cartItem objects into orderItem objects
            for item in cartItems:
                OrderItem(orderID=order, productID=item.productID, quantity=item.quantity).save()
                total += (item.productID.price * item.quantity)
            order.total = total
            order.save()

            # Delete user's `cart`
            # Note: `cart` deletion cascades to `cartItem`
            cart.delete()
            order = Order.objects.filter(userID=request.user).first()
            orderItems = OrderItem.objects.filter(orderID=order)
            return render(request, 'order-complete.html', {'order': order, "orderItems": orderItems})
    else:
        content = {
            'address_form': AddressForm(),
            'payment_form': PaymentForm()
        }
    return render(request, 'checkout.html', content)
