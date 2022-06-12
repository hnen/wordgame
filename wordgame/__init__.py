from flask import Flask
from flask import render_template
from os import getenv

from . import game
from . import admin
from . import index
from . import auth

from . import db

def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/static')

    app.secret_key = getenv("SECRET_KEY")
    app.debug = True

    db.init(app)

    app.register_blueprint(index.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)

    return app

