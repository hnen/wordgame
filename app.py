from flask import Flask
from flask import render_template, jsonify

app = Flask(__name__, static_url_path='/static')
app.secret_key = '715517'
app.debug = True

@app.route('/')
def index():
    return render_template( "index.html" )

@app.route('/game', methods=['GET', 'POST'])
def game():
    return render_template( "game.html" )

@app.route('/action_game_start', methods=['POST'])
def game_start():
    response = { 'word_length': 5 }
    return jsonify( response )


