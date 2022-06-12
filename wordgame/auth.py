from flask import Blueprint, session, request
from flask import render_template, redirect, url_for
from .db import Dao
import re
import hashlib

bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', static_url_path='/static')

class AuthSession:
    KEY_ACCOUNT_ID = "auth_account_id"

    def set_account( self, account_id : int ):
        session[self.KEY_ACCOUNT_ID] = account_id

    def get_account(self) -> int:
        if not self.KEY_ACCOUNT_ID in session:
            return -1
        return session[self.KEY_ACCOUNT_ID]

    def is_logged_in(self):
        return self.get_account() >= 0

    def expire(self):
        session.pop(self.KEY_ACCOUNT_ID, None)

class RegisterInfo:
    username = ""
    password_hash = ""
    is_admin = False

    def __init__(self, username, password_hash, is_admin):
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

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

    username = request.form["account_name"]
    password = request.form["account_pass"]

    dao = Dao()
    acc = dao.get_account_by_username(username)

    if not acc or password_hash(password) != acc.password:
        return redirect(url_for('index.index', error="Väärä käyttäjätunnus tai salasana."))

    session = AuthSession()
    session.set_account(acc.id)

    return redirect(url_for('index.index'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session = AuthSession()
    session.expire()

    return redirect(url_for('index.index'))

def validate_register_input():
    if not request.form:
        return None, None

    print(str(request.form))

    username = request.form["account_name"]
    password_text0 = request.form["account_pass0"]
    password_text1 = request.form["account_pass1"]
    is_admin = request.form["account_admin"] == "on" if "account_admin" in request.form else False

    if not (username and password_text0 and password_text1):
        return None, None

    if password_text0 != password_text1:
        return None, "Salasanat eivät täsmää."

    password_error = validate_password(password_text0)
    if password_error:
        return None, password_error

    return RegisterInfo( username, password_hash(password_text0), is_admin ), None


def validate_password(password_text):
    if len(password_text) < 8:
        return "Salasana on liian lyhyt. Salasanassa tulee olla ainakin 8 merkkiä."

    requirements = [
        ("[a-zåäö]+", "Pieniä kirjaimia"),
        ("[A-ZÅÄÖ]+", "Isoja kirjaimia"),
        ("[0-9]+", "Numeroita"),
        ("[^a-zåäöA-ZÅÄÖ0-9]+", "Erikoismerkkejä tai välilyöntejä")
    ]

    req_count = 0
    req_missing = []
    for req_pattern, req_desc in requirements:
        if re.search(req_pattern, password_text):
            req_count += 1
        else:
            req_missing.append(req_desc)

    req_count_min = 3
    if req_count < req_count_min:
        error = ""
        req_count_missing = req_count_min - req_count
        if req_count_missing == 2:
            error = "Lisää salasanaan vielä ainakin kahta seuraavista: "
        elif req_count_missing == 1:
            error = "Lisää salasanaan vielä ainakin yhdenlaisia seuraavista: "
        else:
            error = "Salasanassa tulee olla vielä " + req_count_missing + ":a seuraavista: " # not really used but is here for future-proofing
        
        return error + "<ul>" + "".join(map(lambda r: "<li>" + r + "</li>", req_missing)) + "</ul>"

    return None
    
def password_hash(password_text):
    return hashlib.sha256(password_text.encode('utf-8')).hexdigest()

