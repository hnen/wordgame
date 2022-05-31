from flask import Blueprint, request
from flask import render_template
from .db import Dao, Theme

bp = Blueprint('admin', __name__, url_prefix='/admin', static_folder='static', static_url_path='/static')

@bp.route('/', methods=['GET', 'POST'])
def admin():
    dao = Dao()
    return render_template( "admin.html", themes=dao.get_themes() )

@bp.route('/themes', methods=['GET', 'POST'])
def themes():
    return render_template( "admin.html" )

@bp.route('/theme/<theme_id>', methods=['GET', 'POST'])
def theme(theme_id):
    return render_template( "admin.html" )

@bp.route('/add', methods=['GET', 'POST'])
def add():
    dao = Dao()

    if request.form["do_add"] == "on":
        do_add(dao, request.form)

    return render_template( "admin_add.html", themes=dao.get_themes() )

def do_add(dao, form):

    print("Adding:", form)

