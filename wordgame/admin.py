from flask import Blueprint, request
from flask import render_template
from .db import Dao, Theme
import re

bp = Blueprint('admin', __name__, url_prefix='/admin', static_folder='static', static_url_path='/static')

@bp.route('/', methods=['GET', 'POST'])
def admin():
    return render_template( "admin.html" )

@bp.route('/themes', methods=['GET', 'POST'])
def themes():
    dao = Dao()
    return render_template( "admin_themes.html", themes=dao.get_themes() )

@bp.route('/theme/<theme_id>', methods=['GET', 'POST'])
def theme(theme_id):
    return render_template( "admin.html" )

@bp.route('/add', methods=['GET', 'POST'])
def add():
    dao = Dao()

    accepted, rejected = [], []

    if "do_add" in request.form and request.form["do_add"] == "on":
        accepted, rejected = do_add(dao, request.form)

    return render_template( "admin_add.html", themes=dao.get_themes(), rejected_words = rejected, accepted_words = accepted )

def do_add(dao, form):
    print("Adding:", form)

    word_list = parse_words(form["word_list"])
    theme_ids = parse_theme_ids(form)
    accepted, rejected = validate_words(word_list)

    print("ACCEPTED: ", str(accepted))
    print("REJECTED: ", str(rejected))
    print("theme ids: ", str(theme_ids))

    dao.add_words( accepted, theme_ids )

    return accepted, rejected
    

def validate_word(word):
    length = len(word)
    if length < 3 or length > 8:
        return False

    if re.search( "[^a-zåäö]", word ):
        return False

    return True
    

def validate_words(word_list):
    rejected = []
    accepted = []
    for word in word_list:
        if validate_word(word):
            accepted.append(word)
        else:
            rejected.append(word)
    return (accepted, rejected)

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

