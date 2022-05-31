from flask import Blueprint
from flask import render_template
from .db import Dao

bp = Blueprint('admin', __name__, url_prefix='/admin', static_folder='static', static_url_path='/static')

@bp.route('/', methods=['GET', 'POST'])
def admin():
    return render_template( "admin.html" )

@bp.route('/themes', methods=['GET', 'POST'])
def themes():
    return render_template( "admin.html" )

@bp.route('/theme/<theme_id>', methods=['GET', 'POST'])
def theme(theme_id):
    return render_template( "admin.html" )

@bp.route('/add', methods=['GET', 'POST'])
def add():
    return render_template( "admin.html" )