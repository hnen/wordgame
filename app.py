from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template( "index.html" )


@app.route("/game", methods=["POST"])
def game():
    return render_template( "game.html" )

