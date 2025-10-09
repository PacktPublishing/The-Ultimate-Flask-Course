import click 

from random import randint, choice

from faker import Faker
from flask.cli import with_appcontext
from sqlalchemy.sql import func

from .extensions import db
from .models import Customer, Order, Product

fake = Faker()

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name='create_products')
@with_appcontext
def create_products():
    product1 = Product(name='First Product', price=10, monthly_goal=1000)
    product2 = Product(name='Second Product', price=25, monthly_goal=4000)
    product3 = Product(name='Third Product', price=90, monthly_goal=3000)

    db.session.add_all([product1, product2, product3])
    db.session.commit()

@click.command(name='create_orders')
@with_appcontext
def create_orders():
    products = Product.query.all()

    for _ in range(100):
        customer = Customer(name=fake.name())
        db.session.add(customer)
        db.session.flush()

        quantity = randint(1, 7)
        product = choice(products)
        date = fake.date_time_between(start_date='-600d', end_date='now')
        
        order = Order(
            customer_id=customer.id, 
            product_id=product.id,
            quantity=quantity,
            date=date
        )

        db.session.add(order)

    db.session.commit()