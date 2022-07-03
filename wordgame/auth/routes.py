from flask import Blueprint, request
from flask import render_template, redirect, url_for
from ..db import Dao
from ..app import app
from .auth import *
from .session import Session

bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', static_url_path='/static')

@app.context_processor
def inject_auth():
    dao = Dao()
    session = Session()
    account = dao.get_account( session.get_account() ) if session.is_logged_in() else None
    return dict(account=account)

@bp.route('/register', methods=['GET', 'POST'])
def register(): 
    username = request.form.get("account_name")
    password_text0 = request.form.get("account_pass0")
    password_text1 = request.form.get("account_pass1")
    is_admin = request.form.get("account_admin") == "on" if "account_admin" in request.form else False

    if not(username and password_text0 and password_text1):
        return render_template( "register.html" )
        
    error = try_register(username, password_text0, password_text1, is_admin)

    if error:
        return render_template( "register.html", error=error )

    return redirect(url_for('index.index', message="Tili luotu onnistuneesti. Voit kirjautua nyt sisään."))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if not ("account_name" in request.form and "account_pass" in request.form):
        return render_template("login.html")

    username = request.form["account_name"]
    password = request.form["account_pass"]    

    if not try_login( username, password ):
        return render_template("login.html", error="Väärä käyttäjätunnus tai salasana. Yritä kirjautua uudestaan, tai <a href='register'>luo tunnus</a>.")

    return redirect(url_for('index.index'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session = Session()
    session.expire()

    return redirect(url_for('index.index'))

