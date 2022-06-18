from flask import Blueprint, request, redirect, url_for, abort
from flask import render_template, jsonify
from ..auth import AuthSession
from ..db import Dao
from .admin import *

bp = Blueprint('admin', __name__, url_prefix='/admin', static_folder='../static', static_url_path='/static')

@bp.before_request
def before_request():
    if not is_user_admin():
        abort(403)

@bp.route('/', methods=['GET', 'POST'])
def admin():
    return render_template( "admin.html" )

@bp.route('/themes', methods=['GET', 'POST'])
def themes():
    dao = Dao()
    return render_template( "admin_themes.html", themes=dao.get_themes() )


@bp.route('/words', methods=['GET', 'POST'])
def words():
    dao = Dao()
    return render_template( "admin_words.html", words=dao.get_all_words() )


@bp.route('/words/remove/<word_id>', methods=['GET', 'POST'])
def word_remove(word_id):
    dao = Dao()
    dao.remove_word(word_id)
    return redirect(url_for('admin.words'))

@bp.route('/words/remove', methods=['GET', 'POST'])
def word_remove_multiple():

    def parse_selected_words(form):
        ret = []
        for (key, value) in form.items():
            match = re.search( "select_\d+", key )
            if match:
                ret.append(int(match.group()[7:]))
        return ret

    dao = Dao()
    word_ids = parse_selected_words(request.form)
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

    def parse_words(words_raw):
        w = words_raw.split("\n")
        w = map( str.strip, w )
        w = map( str.lower, w )
        return list( w )

    def parse_theme_ids(form):
        ret = []
        for (key, value) in form.items():
            if value == "on":
                match = re.search( "theme_\d+", key )
                if match:
                    ret.append(int(match.group()[6:]))
        return ret

    if "do_add" in request.form and request.form["do_add"] == "on":
        accepted, rejected = add_words(parse_words(request.form["word_list"]), parse_theme_ids(request.form))

    return render_template( "admin_add.html", rejected_words = rejected, accepted_words = accepted )