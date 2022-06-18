from flask import Blueprint, request, redirect, url_for, abort
from flask import render_template, jsonify
from ..auth import AuthSession
from ..db import Dao
from .admin import *

bp = Blueprint('admin', __name__, url_prefix='/admin', static_folder='../static', static_url_path='/static')

@bp.before_request
def before_request():
    auth = AuthSession()
    dao = Dao()

    if not auth.is_logged_in():
        abort(403)

    acc_id = auth.get_account()
    acc = dao.get_account(acc_id)

    if not acc or not acc.is_admin:
        abort(403)

@bp.route('/', methods=['GET', 'POST'])
def admin():
    return render_template( "admin.html" )

@bp.route('/themes', methods=['GET', 'POST'])
def themes():
    dao = Dao()

    error = None
    if "error" in request.args:
        error = request.args["error"]

    return render_template( "admin_themes.html", themes=dao.get_themes(), error=error )


@bp.route('/words', methods=['GET', 'POST'])
def words():
    dao = Dao()

    error = None
    if "error" in request.args:
        error = request.args["error"]

    return render_template( "admin_words.html", themes=dao.get_themes(), words=dao.get_all_words(), error=error )


@bp.route('/words/remove/<word_id>', methods=['GET', 'POST'])
def word_remove(word_id):
    dao = Dao()
    dao.remove_word(word_id)
    return redirect(url_for('admin.words'))

@bp.route('/words/remove', methods=['GET', 'POST'])
def word_remove_multiple():
    dao = Dao()
    word_ids = parse_selected_words(request.form)
    print(str(word_ids))
    dao.remove_words(word_ids)
    return redirect(url_for('admin.words'))


@bp.route('/words/add_theme', methods=['POST'])
def word_add_theme():
    dao = Dao()
    word_id = int(request.form["word_id"])
    theme_id = int(request.form["theme_id"])
    dao.add_word_to_theme( theme_id, word_id )
    return jsonify({})

@bp.route('/words/remove_theme', methods=['POST'])
def word_remove_theme():
    dao = Dao()
    word_id = int(request.form["word_id"])
    theme_id = int(request.form["theme_id"])
    dao.remove_word_from_theme( theme_id, word_id )
    return jsonify({})

@bp.route('/words/word_themes', methods=['GET'])
def word_themes():
    dao = Dao()    
    return jsonify({"word_themes": dao.get_word_themes_dict()})

@bp.route('/themes/add', methods=['POST'])
def theme_add():
    dao = Dao()

    theme_name = request.form["theme_name"]
    error = ""
    if not validate_theme(theme_name):
        error = "Teeman nimi ei kelpaa"
    else:
        dao.add_theme( theme_name )

    return redirect(url_for('admin.themes', error=error))

@bp.route('/themes/<theme_id>/remove', methods=['GET', 'POST'])
def theme_remove(theme_id):
    dao = Dao()
    dao.remove_theme(theme_id)
    return redirect(url_for('admin.themes'))

@bp.route('/themes/<theme_id>', methods=['GET', 'POST'])
def theme(theme_id):
    dao = Dao()
    return render_template( "admin_view_theme.html", words=dao.get_words(theme_id), theme=dao.get_theme(theme_id) )

@bp.route('/themes/<theme_id>/remove/<word_id>', methods=['GET', 'POST'])
def theme_remove_word(theme_id, word_id):
    dao = Dao()
    dao.remove_word_from_theme(theme_id, word_id)
    return redirect(url_for('admin.theme', theme_id=theme_id))

@bp.route('/add', methods=['GET', 'POST'])
def add():
    dao = Dao()

    accepted, rejected = [], []

    if "do_add" in request.form and request.form["do_add"] == "on":
        accepted, rejected = do_add(dao, request.form)

    return render_template( "admin_add.html", themes=dao.get_themes(), rejected_words = rejected, accepted_words = accepted )