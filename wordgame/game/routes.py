from flask import Blueprint, session, request, redirect, url_for
from flask import render_template, jsonify
from ..db import Dao
from ..auth import AuthSession
from .game import Game, GuessResult

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
def start():
    theme_id = request.form["theme_id"]

    game = Game()
    game.start(theme_id)
    word_obj = game.get_current_word()        
    
    response = { 
        'word_length': len(word_obj.word), 
        'id': word_obj.id, 
        'time_left_ms': game.get_time_left(),
        'correct_points': game.get_points_for_curr_guess(),
        'points': game.get_points()
    }

    return jsonify( response )

@bp.route('/', methods=['GET', 'POST'])
def index():
    dao = Dao()
    return render_template( "game_index.html" )

@bp.route('/guess', methods=['POST'])
def guess():
    game = Game()

    if not 'guess' in request.form:
        return "Guess not supplied", 400

    guess = request.form['guess']

    word_before = game.get_current_word()
    prev_points = game.get_points()
    status, result = game.guess(guess)
    word = game.get_current_word()

    if status == GuessResult.INVALID:
        return {"status": "invalid_guess"}
    elif status == GuessResult.GAME_OVER:
        return { 'status': 'game_over', 'points': game.get_points() }
    elif status == GuessResult.WRONG:
        status = "try_again"
    elif status ==  GuessResult.RIGHT:
        status = "new_word"
    else:
        raise Exception(f"Invalid status: {status}")

        response = { 
            'status': status, 
            'word_id': word.id, 
            'word_length': len(word.word), 
            'guess': request.form['guess'], 
            'result': result, 
            'time_left_ms': game.get_time_left(),
            'got_points': game.get_points() - prev_points,
            'correct_points': game.get_points_for_curr_guess(),
            'points': game.get_points()
        }
        return jsonify( response )
    else:
        raise Exception("Unexpected status from Game.guess " + str(status))

