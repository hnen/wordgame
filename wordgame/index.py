from flask import Blueprint, render_template, request
from .db import Dao
from .auth import AuthSession
import html

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    dao = Dao()

    message = html.escape(request.args["message"]) if request and "message" in request.args else None
    error = html.escape(request.args["error"]) if request and "error" in request.args else None

    session = AuthSession()
    account = session.get_account() if session.is_logged_in() else None

    return render_template( "index.html", themes=dao.get_themes(), message=message, error=error, account=account )
