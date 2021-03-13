from django.forms import ModelForm, ModelChoiceField
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.categoryName


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['categoryName', 'categoryDetails']

        labels = {
            'categoryName': 'Category Name',
            'categoryDetails': 'Category Details'
        }


class ProductForm(ModelForm):
    category = CategoryChoiceField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ["productName", "productDetails", "category", "stock", "price", "picture"]

        labels = {
            'productName': 'Product Name',
            'productDetails': 'Product Details'
        }


class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "contactNum"]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'contactNum': 'Contact Number'
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.isAdmin = False
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init_(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'howdy'}))


class AddressForm(ModelForm):
    class Meta:
        model = Address
        widget = {
            'line1': forms.TextInput(attrs={'class': 'form-control'}),
            'line2': forms.TextInput(attrs={'class': 'form-control'}),
            'line3': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
        }

        fields = ["line1", "line2", "line3", "postcode"]

        labels = {
            'line1': 'Address-line 1',
            'line2': 'Address-line 2',
            'line3': 'Address-line 3',
            'postcode': 'Postcode'
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ["holderName", "cardNum", "expireMonth", "expireYear", "cvv"]

        labels = {
            'holderName': 'Card Owner Name',
            'cardNum': 'Card Number',
            'expireMonth': 'Expire Month',
            'expireYear': 'Expire Year',
            'cvv': 'CVV'
        }
