import factory
from factory.django import DjangoModelFactory

from account.models import CustomUser
from product.models import Product
from .models import Cart, CartItem


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(CustomUser)
    status = 'ACTIVE'
    currency = 'PLN'


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem
    
    cart = factory.SubFactory(Cart)
    product =  factory.SubFactory(Product)
    amount = factory.Faker('pyint', min_value=1, max_value=10)
