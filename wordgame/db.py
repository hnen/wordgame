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

class Theme:
    id = -1
    name = ""

    def __init__(self, theme_id : int, name : str):
        self.id = theme_id
        self.name = name

class Dao:
    def _unpack_word(self, result) -> Word:
        tp = result.fetchone()._mapping
        return Word( tp["id"], tp["word"] )

    def _unpack_themes(self, result) -> []:
        ret = []
        for tp in result.fetchall():            
            mapping = tp._mapping
            ret.append(Theme(mapping["id"], mapping["theme_name"]))
        return ret

    def select_random_word(self) -> Word:
        # TODO: This method is slow, should come up with something more efficient.
        result = db.session.execute("SELECT * FROM word ORDER BY RANDOM() LIMIT 1")
        return self._unpack_word(result)

    def get_word(self, word_id : int) -> Word:
        result = db.session.execute("SELECT * FROM word WHERE id = :id", {"id": word_id})
        return self._unpack_word(result)

    def get_themes(self) -> []:
        result = db.session.execute("SELECT * FROM theme")
        return self._unpack_themes(result)



