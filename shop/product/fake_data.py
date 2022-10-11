from faker import Faker
from models import Product

fake = Faker()
fake.seed(0)

def generate_product_data():
    prod = Product(
        name=fake.word().capitalize(),
        price=fake.pyint(),
        description=fake.text(max_mb_chars=100),
        category=fake.pyint(1, 10), 
    )

    prod.save()


if __name__ == '__main__':
    generate_product_data()
