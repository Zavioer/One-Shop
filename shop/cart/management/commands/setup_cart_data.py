import random

from django.db import transaction
from django.core.management.base import BaseCommand

from cart.factories import CartFactory, CartItemFactory, CustomUser, Product


class Command(BaseCommand):
    help = 'Generate dummy data for testing cart logic'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Creating new dummy data for cart logic...')

        products = Product.objects.all()
        user = CustomUser.objects.get(pk=1)
        cart = CartFactory(user=user)

        for _ in range(5):
            product = random.choice(products)
            CartItemFactory(cart=cart, product=product)
