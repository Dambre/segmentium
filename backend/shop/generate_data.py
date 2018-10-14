import random

from faker import Faker

from .random import random_names
from .models import Order, Customer, Product


def generate_orders():
    products = Product.objects.all()
    counter = 0
    while True:
        counter += 1
        print(counter)

        datetime = Faker().date_time_between(start_date='-1y', end_date='now')
        if random.choice(range(0, 10)) == 9:
            customer = Customer.objects.create(name=random.choice(random_names))
            print('new customer')
        else:
            count = Customer.objects.count()
            customer = Customer.objects.all()[random.randint(0, count - 1)]

        Order.objects.create(
            customer=customer,
            product=random.choice(products),
            created_at=datetime,
        )
