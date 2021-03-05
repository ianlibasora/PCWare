
from . import views
from django.urls import path, include
from .forms import UserLoginForm

urlpatterns = [
    path('', views.index, name="index-page"),
    path("all-products/", views.allProducts, name="all-products"),
    path('single-product/<int:prodId>/', views.singleProduct, name='single-product'),

    # Forms
    path('category-form/', views.productCategoryForm, name='category-form'),
    path("product-form/", views.productForm, name="product-form"),

    # Register/Login views
    path("register/", views.UserSignUp.as_view(), name="registration-page"),
    path('login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_view, name="logout"),

    # Shop urls
    path("add-cart/<int:productID>", views.addCart, name="Add to cart"),

    # Payment/Address
    path("view-basket/", views.showBasket, name="basket"),
    path("checkout/", views.getCheckout, name="checkout page"),
]
