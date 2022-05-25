from flask import Flask
from flask import render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__, static_url_path='/static')
app.secret_key = '715517'
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template( "index.html" )

@app.route('/game', methods=['GET', 'POST'])
def game():
    return render_template( "game.html" )

@app.route('/action_game_start', methods=['POST'])
def game_start():
    result = db.session.execute("SELECT word FROM word LIMIT 1")
    word = result.fetchone()._mapping["word"]
    response = { 'word_length': len(word), 'word': word }
    return jsonify( response )


