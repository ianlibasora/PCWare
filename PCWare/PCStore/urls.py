
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name="index-page"),
    path("register", views.register, name="registration-page")
]

