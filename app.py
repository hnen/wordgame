from flask import Flask, session
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

    def is_active():
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
        self.word_id = word_id
        self.word = word

class UserDao:
    def _unpack_word(self, result) -> Word:
        tp = result.fetchone()._mapping
        return Word( tp["id"], tp["word"] )

    def select_random_word(self) -> Word:
        # TODO: This method is slow, should come up with something more efficient.
        result = db.session.execute("SELECT * FROM word ORDER BY RANDOM() LIMIT 1")
        return self._unpack_word(result)

@app.route('/game/start', methods=['POST'])
def game_start():
    game_session = GameSession()
    dao = UserDao()

    word = dao.select_random_word()
    game_session.start(word.id)
    
    response = { 'word_length': len(word.word), 'word': word.word }
    return jsonify( response )


