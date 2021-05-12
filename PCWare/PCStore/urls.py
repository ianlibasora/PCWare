from rest_framework import routers
from . import views
from django.urls import path, include
from .forms import UserLoginForm
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"orders", views.OrderViewSet)
# router.register(r"register", views.RegisterViewSet)

urlpatterns = [
    path('', views.index, name="index-page"),
    path("all-products/", views.allProducts, name="all-products"),
    path('single-product/<int:prodId>/', views.singleProduct, name='single-product'),

    # Account
    path("account/", views.userHomeView, name="User home page"),

    # Admin only links
    path('account/category-form/', views.productCategoryForm, name='Category-form'),
    path("account/product-form/", views.productForm, name="Product-form"),
    path("account/admin-view-orders/", views.adminViewOrders, name="Admin order overview"),
    path("account/admin-view-orders/order-info/<int:orderID>", views.adminOrderMoreInfo, name="Admin order more info"),

    # All users
    path("account/my-orders/", views.myOrders, name="View all user's orders"),
    path("account/my-orders/order-info/<int:orderID>", views.myOrderInfo, name="View myorder more info"),
    path("account/register/", views.UserSignUp.as_view(), name="registration-page"),
    path('account/login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('account/logout/', views.logout_view, name="logout"),

    # Shop urls
    path("basket/add-cart/<int:productID>", views.addCart, name="Add to cart"),
    path("basket/remove-cart/<int:productID>", views.removeCart, name="Remove from cart"),
    path("basket/view-basket/", views.showBasket, name="Basket"),
    path("basket/view-basket/checkout/", views.getCheckout, name="Checkout page"),

    # API endpoints
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path('token/', obtain_auth_token, name="api_token_auth"),

    path("test/register/", views.RegistrationView, name="Test reg")
]
