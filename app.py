from flask import Flask, session, request
from flask import render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__, static_url_path='/static')
app.secret_key = getenv("SECRET_KEY")
app.debug = True

uri = getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template( "index.html" )

@app.route('/game', methods=['GET', 'POST'])
def game():
    return render_template( "game.html" )

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

class Word:
    id = -1
    word = ""

    def __init__(self, word_id : int, word : str):
        self.id = word_id
        self.word = word

class Dao:
    def _unpack_word(self, result) -> Word:
        tp = result.fetchone()._mapping
        return Word( tp["id"], tp["word"] )

    def select_random_word(self) -> Word:
        # TODO: This method is slow, should come up with something more efficient.
        result = db.session.execute("SELECT * FROM word ORDER BY RANDOM() LIMIT 1")
        return self._unpack_word(result)

    def get_word(self, word_id : int) -> Word:
        result = db.session.execute("SELECT * FROM word WHERE id = :id", {"id": word_id})
        return self._unpack_word(result)

@app.route('/game/start', methods=['POST'])
def game_start():
    game_session = GameSession()
    dao = Dao()

    word = dao.select_random_word()
    game_session.start(word.id)
    
    response = { 'word_length': len(word.word), 'word': word.word, 'id': word.id }
    return jsonify( response )

def evaluate_guess(guess : str, word : str):
    if len(guess) != len(word):
        return []

    result = [ "WRONG" ] * len(word)
    
    char_map = {}
    for c in range(ord('a'), ord('z')):
        char_map[chr(c)] = 0

    for i in range(len(word)):
        word_c = word[i].lower()
        char_map[word_c] += 1

    for i in range(len(word)):
        word_c = word[i].lower()
        if word[i].lower() == guess[i].lower():
            char_map[word_c] -= 1
            result[i] = "CORRECT"

    for i in range(len(word)):
        word_c = word[i].lower()
        guess_c = guess[i].lower()
        if word[i].lower() != guess[i].lower() and char_map[guess_c] > 0:
            char_map[guess_c] -= 1
            result[i] = "HINT"

    return result
    

@app.route('/game/guess', methods=['POST'])
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

    response = { 'word_id': game_session.get_word_id(), 'word': word_obj.word, 'guess': request.form['guess'], 'result': result }
    return jsonify( response )

