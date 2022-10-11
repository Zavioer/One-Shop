from typing import *
import random 

from django.db import transaction
from django.core.management.base import BaseCommand

from product.factories import ProductFactory, CategoryFactory


class Command(BaseCommand):
    help = 'Generate dummy data for testing'

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Creating new dummy data...')

        categories = []
        for _ in range(5):
            category = CategoryFactory()
            categories.append(category)

        for _ in range(25):
            category = random.choice(categories)
            product = ProductFactory(category=category)
            
