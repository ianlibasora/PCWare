from django.forms import ModelForm
from .models import *


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = {'categoryName', 'categoryDetails'}
