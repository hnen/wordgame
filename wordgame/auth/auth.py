from ..db import Dao
from .session import Session
import re
import hashlib

def try_login(username, password):    
    dao = Dao()
    acc = dao.get_account_by_username(username)

    if not acc or password_hash(password) != acc.password:
        #return render_template("login.html", error="Väärä käyttäjätunnus tai salasana. Yritä kirjautua uudestaan, tai <a href='register'>luo tunnus</a>.")
        return False

    session = Session()
    session.set_account(acc.id)

    return True

def try_register(username, password_text0, password_text1, is_admin):
    if not (username and password_text0 and password_text1):
        return "Virheellinen syöte"

    if password_text0 != password_text1:
        return "Salasanat eivät täsmää."

    password_error = validate_password(password_text0)
    if password_error:
        return password_error

    dao = Dao()
    if dao.get_account_by_username(username):
        return "Käyttäjätunnus on jo varattu. Kokeile rekisteröityä toisella käyttäjänimellä."

    dao.add_account( username, password_hash(password_text0), is_admin )

    return None

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

