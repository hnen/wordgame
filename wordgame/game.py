from flask import Blueprint, session, request
from flask import render_template, jsonify
from .db import Dao, Word
import time

bp = Blueprint('game', __name__, url_prefix='/game', static_folder='static', static_url_path='/static')

GAME_DURATION_S = 120

class GameSession:
    KEY_WORD_ID = "game_word_id"
    KEY_THEME_ID = "game_theme_id"
    KEY_START_TIME = "game_start_time"
    KEY_GUESS_COUNT = "game_guess_count"
    KEY_POINTS = "game_points"

    def is_active(self):
        return (self.KEY_WORD_ID in session) and session[self.KEY_WORD_ID] > 0

    def get_word_id(self):
        if self.is_active():
            return session[self.KEY_WORD_ID]
        return -1

    def set_word_id(self, id : int):
        session[self.KEY_WORD_ID] = id

    def set_theme_id(self, id : int):
        session[self.KEY_THEME_ID] = id

    def set_guess_count(self, cnt : int):
        session[self.KEY_GUESS_COUNT] = cnt

    def set_points(self, points : int):
        session[self.KEY_POINTS] = points

    def get_theme_id(self):
        return session[self.KEY_THEME_ID]

    def get_guess_count(self):
        return session[self.KEY_GUESS_COUNT]

    def get_points(self):
        return session[self.KEY_POINTS]

    def set_start_time(self, time : int):
        session[self.KEY_START_TIME] = time

    def get_start_time(self):
        return int(session[self.KEY_START_TIME])

    def start(self, theme_id, word_id, start_time):
        self.set_theme_id(theme_id)
        self.set_word_id(word_id)
        self.set_start_time(start_time)
        self.set_guess_count(0)
        self.set_points(0)

    def expire(self):
        session.pop(self.KEY_WORD_ID, None)
        session.pop(self.KEY_THEME_ID, None)
        session.pop(self.KEY_START_TIME, None)

@bp.route('/<theme_id>', methods=['GET', 'POST'])
def game(theme_id):
    return render_template( "game.html", theme_id=theme_id )

@bp.route('/start', methods=['POST'])
def game_start():
    game_session = GameSession()
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

@bp.route('/guess', methods=['POST'])
def game_guess():
    game_session = GameSession()
    dao = Dao()

    if not game_session.is_active():
        return "Game not active", 400

    if not 'guess' in request.form:
        return "Guess not supplied", 400

    guess = request.form['guess']
    word_obj = dao.get_word( game_session.get_word_id() )

    if len(guess) != len(word_obj.word):
        return "Guess has invalid length, expected: " + len(word_obj.word), 400

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

    time_left_ms = GAME_DURATION_S * 1000 - (time.time_ns() - game_session.get_start_time()) / 1_000_000;

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

def points_for_guess(guess_num : int):
    point_table = [10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    return point_table[min(guess_num, len(point_table) - 1)]

def is_correct(result):
    return all( r == "CORRECT" for r in result )

def evaluate_guess(guess : str, word : str):
    if len(guess) != len(word):
        return []

    result = [ "WRONG" ] * len(word)
    
    char_map = {}
    for c in range(ord('a'), ord('z') + 1):
        char_map[chr(c)] = 0
    char_map['ä'] = 0
    char_map['ö'] = 0
    char_map['å'] = 0

    for i in range(len(word)):
        word_c = word[i].lower()
        char_map[word_c] += 1

    # Check letters in right position
    for i in range(len(word)):
        word_c = word[i].lower()
        if word[i].lower() == guess[i].lower():
            char_map[word_c] -= 1
            result[i] = "CORRECT"

    # Check letters in wrong position
    for i in range(len(word)):
        word_c = word[i].lower()
        guess_c = guess[i].lower()
        if word[i].lower() != guess[i].lower() and char_map[guess_c] > 0:
            char_map[guess_c] -= 1
            result[i] = "HINT"

    return result
    
