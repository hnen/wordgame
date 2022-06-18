from flask import request
import re
import hashlib

class RegisterInfo:
    username = ""
    password_hash = ""
    is_admin = False

    def __init__(self, username, password_hash, is_admin):
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

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

