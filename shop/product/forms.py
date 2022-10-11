from dataclasses import field
from django.forms import ModelForm
from .models import Product, Category, Comment


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
