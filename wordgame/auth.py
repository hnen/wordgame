from flask import Blueprint, session, request
from flask import render_template
from .db import Dao
import time

bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', static_url_path='/static')

class AuthSession:
    KEY_ACCOUNT_ID = "auth_account_id"

    def set_account( account_id : int ):
        session[self.KEY_ACCOUNT_ID] = account_id

    def get_account() -> int:
        if not self.KEY_ACCOUNT_ID in session:
            return -1
        return session[self.KEY_ACCOUNT_ID]

    def expire():
        session.pop(self.KEY_ACCOUNT_ID, None)

@bp.route('/register', methods=['GET', 'POST'])
def register( username : str, password : str, is_admin : bool ):
    dao = Dao()
    dao.add_account( username, password, is_admin )
    return login( username, password )

@bp.route('/login', methods=['GET', 'POST'])
def login( username : str, password : str ):
    dao = Dao()
    acc = get_account_by_name(username)

    if not acc:
        return "Invalid username or password", 403

    return redirect(url_for('index'))



