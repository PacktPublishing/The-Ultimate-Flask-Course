import click 

from flask.cli import with_appcontext

from .extensions import db
from .models import Customer, Order, Product

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()