from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name="index"),  # /app
    path('registration/', views.register, name="register")  # /app/registration
]
