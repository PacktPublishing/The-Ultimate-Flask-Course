from flask import Flask 

from .routes.auth import auth
from .routes.main import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app