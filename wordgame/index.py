from flask import Blueprint, render_template
from .db import Dao

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    dao = Dao()
    return render_template( "index.html", themes=dao.get_themes() )
