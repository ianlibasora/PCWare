from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = {'categoryName', 'categoryDetails'}


class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.isAdmin = False
        user.save()
        return user
