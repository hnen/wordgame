from flask import Blueprint, session, request, redirect, url_for
from flask import render_template, jsonify
from ..db import Dao, Word
from ..auth import AuthSession
from .session import Session
from .game import *
import time

bp = Blueprint('game', __name__, url_prefix='/game', static_folder='../static', static_url_path='/static')

@bp.before_request
def before_request():
    auth = AuthSession()

    if not auth.is_logged_in():
        return redirect(url_for('auth.login', message="Sinun tulee olla kirjautunut sisään pelataksesi. Kirjaudu sisään alla tai luo tunnus."))

@bp.route('/<theme_id>', methods=['GET', 'POST'])
def game(theme_id):
    dao = Dao()
    return render_template( "game.html", theme=dao.get_theme(theme_id) )

@bp.route('/start', methods=['POST'])
def game_start():
    game_session = Session()
    dao = Dao()
    
    theme_id = request.form["theme_id"]
    word_obj = dao.select_random_word(theme_id)
    game_session.start(theme_id, word_obj.id, time.time_ns())
    
    response = { 
        'word_length': len(word_obj.word), 
        'id': word_obj.id, 
        'time_left_ms': GAME_DURATION_S * 1000,
        'correct_points': points_for_guess(game_session.get_guess_count()),
        'points': game_session.get_points()
    }
    return jsonify( response )

@bp.route('/', methods=['GET', 'POST'])
def game_index():
    dao = Dao()
    return render_template( "game_index.html" )

@bp.route('/guess', methods=['POST'])
def game_guess():
    game_session = Session()
    auth_session = AuthSession()
    dao = Dao()

    if not game_session.is_active():
        return "Game not active", 400

    if get_time_left() <= 0:
        final_points = game_session.get_points()
        dao.add_result(auth_session.get_account(), game_session.get_theme_id(), final_points)
        game_session.expire()
        return { 'status': 'game_over', 'points': final_points }

    if not 'guess' in request.form:
        return "Guess not supplied", 400

    guess = request.form['guess']
    word_obj = dao.get_word( game_session.get_word_id() )

    if len(guess) != len(word_obj.word):
        return {"status": "invalid_guess"};

    result = evaluate_guess( guess, word_obj.word )

    status = "try_again"
    got_points = 0
    correct_points = 0

    if is_correct(result):
        theme_id = game_session.get_theme_id()
        word_obj = dao.select_random_word(theme_id)
        game_session.set_word_id( word_obj.id )
        got_points = points_for_guess( game_session.get_guess_count() )
        game_session.set_points( game_session.get_points() + got_points )
        game_session.set_guess_count(0)
        status = "new_word"
    else:
        game_session.set_guess_count(game_session.get_guess_count() + 1)

    time_left_ms = get_time_left();

    response = { 
        'status': status, 
        'word_id': game_session.get_word_id(), 
        'word_length': len(word_obj.word), 
        'guess': request.form['guess'], 
        'result': result, 
        'time_left_ms': time_left_ms,
        'got_points': got_points,
        'correct_points': points_for_guess(game_session.get_guess_count()),
        'points': game_session.get_points()
    }
    return jsonify( response )