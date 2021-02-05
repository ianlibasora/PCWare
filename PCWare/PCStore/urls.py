
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name="index-page"),
    path("register/", views.register, name="registration-page"),
    path("all-products/", views.allProducts, name="all-products"),
    path('singleproduct/<int:prodId>/', views.singleProduct, name='single-product'),
    path('category-form/', views.productCategoryForm, name='category-form'),
]
