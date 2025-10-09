from flask import Flask 

from .commands import create_tables, create_products, create_orders
from .extensions import db, login_manager
from .models import User
from .routes.auth import auth
from .routes.main import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(auth)
    app.register_blueprint(main)

    app.cli.add_command(create_tables)
    app.cli.add_command(create_products)
    app.cli.add_command(create_orders)

    return app