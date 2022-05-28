from flask import Blueprint, session, request
from flask import render_template, jsonify
from .db import Dao, Word

bp = Blueprint('game', __name__, url_prefix='/game', static_folder='static', static_url_path='/static')

class GameSession:
    KEY_WORD_ID = "game_word_id"

    def is_active(self):
        return (self.KEY_WORD_ID in session) and session[self.KEY_WORD_ID] > 0

    def get_word_id(self):
        if self.is_active():
            return session[self.KEY_WORD_ID]
        return -1

    def set_word_id(self, id : int):
        session[self.KEY_WORD_ID] = id

    def start(self, word_id):
        self.set_word_id(word_id)

    def expire(self):
        session.pop(self.KEY_WORD_ID, None)

@bp.route('/', methods=['GET', 'POST'])
def game():
    return render_template( "game.html" )

@bp.route('/start', methods=['POST'])
def game_start():
    game_session = GameSession()
    dao = Dao()

    word_obj = dao.select_random_word()
    game_session.start(word_obj.id)
    
    response = { 'word_length': len(word_obj.word), 'id': word_obj.id }
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

    response = { 'word_id': game_session.get_word_id(), 'guess': request.form['guess'], 'result': result }
    return jsonify( response )


def evaluate_guess(guess : str, word : str):
    if len(guess) != len(word):
        return []

    result = [ "WRONG" ] * len(word)
    
    char_map = {}
    for c in range(ord('a'), ord('z') + 1):
        char_map[chr(c)] = 0

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
    
