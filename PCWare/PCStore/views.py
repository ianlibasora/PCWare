from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from .models import *
from .forms import *
from django.http import HttpResponse
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
