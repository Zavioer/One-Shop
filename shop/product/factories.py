import factory
from factory.django import DjangoModelFactory
from .models import Product, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('color_name')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    category = factory.SubFactory(CategoryFactory)
    name = 'Product'
    price = factory.Faker('pyfloat', min_value=0)
    description = factory.Faker('paragraph', nb_sentences=3)
