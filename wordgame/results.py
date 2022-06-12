from flask import Blueprint, render_template, request
from .db import Dao
import html

bp = Blueprint('results', __name__, url_prefix='/results', static_folder='static', static_url_path='/static')

@bp.route('/<theme_id>')
def results(theme_id : int):
    dao = Dao()
    theme = dao.get_theme( theme_id )
    return render_template( "results.html", results=dao.get_top_results(theme_id, 10), theme=theme )
