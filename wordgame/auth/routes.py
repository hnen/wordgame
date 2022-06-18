from flask import Blueprint, session, request
from flask import render_template, redirect, url_for
from ..db import Dao
from ..app import app
from .auth import *
from .session import Session
import re
import hashlib

bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', static_url_path='/static')

@app.context_processor
def inject_auth():
    dao = Dao()
    session = Session()
    account = dao.get_account( session.get_account() ) if session.is_logged_in() else None
    return dict(account=account)

@bp.route('/register', methods=['GET', 'POST'])
def register():    
    register_info, error = validate_register_input()

    if not register_info or error:
        return render_template( "register.html", error=error )

    dao = Dao()
    if dao.get_account_by_username(register_info.username):
        return render_template( "register.html", error="Käyttäjätunnus on jo varattu. Kokeile rekisteröityä toisella käyttäjänimellä." )

    dao.add_account( register_info.username, register_info.password_hash, register_info.is_admin )

    return redirect(url_for('index.index', message="Tili luotu onnistuneesti. Voit kirjautua nyt sisään."))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if not ("account_name" in request.form and "account_pass" in request.form):
        return render_template("login.html")

    username = request.form["account_name"]
    password = request.form["account_pass"]

    dao = Dao()
    acc = dao.get_account_by_username(username)

    if not acc or password_hash(password) != acc.password:
        return render_template("login.html", error="Väärä käyttäjätunnus tai salasana. Yritä kirjautua uudestaan, tai <a href='register'>luo tunnus</a>.")

    session = Session()
    session.set_account(acc.id)

    return redirect(url_for('index.index'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session = Session()
    session.expire()

    return redirect(url_for('index.index'))

