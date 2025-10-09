from flask import Blueprint

from .models import MyModel 
from .extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "<h1>Using Blueprint</h1>"