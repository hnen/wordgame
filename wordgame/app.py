from flask import Flask, request, session, abort
from flask import render_template
from os import getenv
import html
from . import db
from .db import Dao

app = Flask(__name__, static_url_path='/static')

app.secret_key = getenv("SECRET_KEY")
app.debug = True

db.init(app)

from . import game
from . import admin
from . import index
from . import auth
from . import results

from .auth import AuthSession

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

@app.context_processor
def inject_themes():
    dao = Dao()
    return dict(themes=dao.get_themes())

@app.context_processor
def inject_csrf_token():    
    auth_session = AuthSession()
    if auth_session.is_logged_in():
        return dict(csrf_token=auth_session.get_csrf_token())
    else:
        return dict()


@app.before_request
def validate_csrf_token():
    auth_session = AuthSession()
    if auth_session.is_logged_in() and request.method == "POST":
        if "csrf_token" not in request.form or len(request.form["csrf_token"]) == 0 or request.form["csrf_token"] != auth_session.get_csrf_token():
            abort(403)
    

