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

    def _unpack_words(self, result) -> []:
        ret = []
        for tp in result.fetchall():            
            mapping = tp._mapping
            ret.append(Word( tp["id"], tp["word"]))
        return ret        

    def _unpack_theme(self, result) -> Word:
        tp = result.fetchone()._mapping
        return Theme(tp["id"], tp["theme_name"], tp["word_count"])

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

    def _theme_query(self):
        return """ SELECT t.*, c.word_count FROM theme t 
                    LEFT JOIN (
                       SELECT theme_id, count(theme_id) word_count FROM word_theme GROUP BY theme_id
                    ) AS c 
                    ON t.id = c.theme_id"""

    def get_themes(self) -> []:
        result = db.session.execute(self._theme_query())
        return self._unpack_themes(result)

    def get_theme(self, theme_id) -> []:
        query = f'{self._theme_query()} WHERE id=:id'
        result = db.session.execute(query, {"id": theme_id})
        return self._unpack_theme(result)

    def get_words(self, theme_id) -> []:
        query = """ SELECT w.id, w.word FROM word w
                    RIGHT JOIN (
                        SELECT * FROM word_theme WHERE theme_id = :theme_id
                    ) as wt
                    ON w.id = wt.word_id"""
        result = db.session.execute(query, {"theme_id": theme_id} )
        return self._unpack_words(result)

    def add_words(self, word_list, theme_ids):
        for word in word_list:
            query1 = "INSERT INTO word VALUES ( DEFAULT, :word ) ON CONFLICT DO NOTHING"
            db.session.execute( query1, {"word": word} )
            for theme_id in theme_ids:
                query2 = """ INSERT INTO word_theme VALUES (
                    DEFAULT,
                    ( SELECT id FROM word WHERE word=:word ),
                    :theme_id
                )  ON CONFLICT DO NOTHING """
                db.session.execute( query2, {"word": word, "theme_id": theme_id} )
        db.session.commit()






