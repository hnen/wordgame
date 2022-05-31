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
    word_count = 0

    def __init__(self, theme_id : int, name : str, word_count : int):
        self.id = theme_id
        self.name = name
        self.word_count = word_count

class Dao:
    def _unpack_word(self, result) -> Word:
        tp = result.fetchone()._mapping
        return Word( tp["id"], tp["word"] )

    def _unpack_themes(self, result) -> []:
        ret = []
        for tp in result.fetchall():            
            mapping = tp._mapping
            ret.append(Theme(mapping["id"], mapping["theme_name"], mapping["word_count"]))
        return ret

    def select_random_word(self) -> Word:
        # TODO: This method is slow, should come up with something more efficient.
        result = db.session.execute("SELECT * FROM word ORDER BY RANDOM() LIMIT 1")
        return self._unpack_word(result)

    def get_word(self, word_id : int) -> Word:
        result = db.session.execute("SELECT * FROM word WHERE id = :id", {"id": word_id})
        return self._unpack_word(result)

    def get_themes(self) -> []:
        query = """ SELECT t.*, c.word_count FROM theme t 
                    LEFT JOIN (
                       SELECT theme_id, count(theme_id) word_count FROM word_theme GROUP BY theme_id
                    ) AS c 
                    ON t.id = c.theme_id"""
        result = db.session.execute(query)
        return self._unpack_themes(result)



