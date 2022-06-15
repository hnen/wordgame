from flask import Flask, request
from flask import render_template
from os import getenv
import html
from . import db

app = Flask(__name__, static_url_path='/static')

app.secret_key = getenv("SECRET_KEY")
app.debug = True

db.init(app)

from . import game
from . import admin
from . import index
from . import auth
from . import results

app.register_blueprint(index.bp)
app.register_blueprint(game.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(results.bp)

@app.context_processor
def inject_messages():
    message = html.escape(request.args["message"]) if request and "message" in request.args else None
    error = html.escape(request.args["error"]) if request and "error" in request.args else None
    return dict(message=message, error=error)
