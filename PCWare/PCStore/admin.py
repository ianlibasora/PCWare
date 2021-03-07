from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)

User = get_user_model()
admin.site.register(User)
