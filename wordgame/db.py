from os import getenv
from flask_sqlalchemy import SQLAlchemy

db = None

def init(app):
    global db

    uri = getenv("DATABASE_URL")

    # Hack that will fix the deprecated URI Heroku uses
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    db = SQLAlchemy(app)

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
