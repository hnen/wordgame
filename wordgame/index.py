from flask import Blueprint, render_template, request
from .db import Dao
from .auth import AuthSession
import html

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    dao = Dao()

    return render_template( "index.html", themes=dao.get_themes() )
