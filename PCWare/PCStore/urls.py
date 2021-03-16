from rest_framework import routers
from . import views
from django.urls import path, include
from .forms import UserLoginForm
from .views import *

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"products", views.ProductViewSet)

urlpatterns = [
    path('', views.index, name="index-page"),#
    path("all-products/", views.allProducts, name="all-products"),#done
    path('single-product/<int:prodId>/', views.singleProduct, name='single-product'),#done

    # Admin / Forms
    path("admin-home/", views.adminHomeView, name="Admin home page"),#done
    path('admin-home/category-form/', views.productCategoryForm, name='category-form'),#
    path("admin-home/product-form/", views.productForm, name="product-form"),#
    path("admin-home/view-orders/", views.viewOrders, name="Admin order overview"),#done
    path("admin-home/view-orders/order-info/<int:orderID>", views.orderMoreInfo, name="Admin order more info"),#done

    # Register/Login views
    path("register/", views.UserSignUp.as_view(), name="registration-page"),#
    path('login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),#
    path('logout/', views.logout_view, name="logout"),#

    # Shop urls
    path("basket/add-cart/<int:productID>", views.addCart, name="Add to cart"),#done
    path("basket/remove-cart/<int:productID>", views.removeCart, name="Remove from cart"),  # done
    path("basket/view-basket/", views.showBasket, name="Basket"),#done
    path("basket/view-basket/checkout/", views.getCheckout, name="Checkout page"),#done

    # API endpoints
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls))
]
