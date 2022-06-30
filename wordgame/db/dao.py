from .structs import *
from .db import get_session

class Dao:

    def _unpack_account(self, result) -> Account:
        row = result.fetchone() 
        if row:
            tp = row._mapping
            return Account( tp["id"], tp["username"], tp["pass"], tp["is_admin"] )
        else:
            return None

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

    def _unpack_results(self, result) -> []:
        ret = []
        for tp in result.fetchall():            
            mapping = tp._mapping
            ret.append(Result( mapping["position"], mapping["username"], mapping["score"] ))
        return ret

    def _unpack_word_themes_dict(self, result) -> []:
        ret = []
        for tp in result.fetchall():            
            mapping = tp._mapping
            ret.append({ "theme_id": mapping["theme_id"], "word_id": mapping["word_id"] })
        return ret

    def select_random_word(self, theme_id) -> Word:
        # TODO: This method is slow, should come up with something more efficient.
        query = "SELECT w.* FROM word w RIGHT JOIN (SELECT * FROM word_theme WHERE theme_id=:theme_id) AS wt ON wt.word_id = w.id ORDER BY RANDOM() LIMIT 1"
        result = get_session().execute(query, {"theme_id": theme_id})
        return self._unpack_word(result)

    def get_word(self, word_id : int) -> Word:
        result = get_session().execute("SELECT * FROM word WHERE id = :id", {"id": word_id})
        return self._unpack_word(result)

    def _theme_query(self):
        return """ SELECT t.*, c.word_count FROM theme t 
                    LEFT JOIN (
                       SELECT theme_id, count(theme_id) word_count FROM word_theme GROUP BY theme_id
                    ) AS c 
                    ON t.id = c.theme_id"""

    def get_themes(self) -> []:
        result = get_session().execute(self._theme_query())
        return self._unpack_themes(result)

    def get_word_themes_dict(self) -> []:
        result = get_session().execute("SELECT * FROM word_theme")
        return self._unpack_word_themes_dict(result)

    def get_theme(self, theme_id) -> []:
        query = f'{self._theme_query()} WHERE id=:id'
        result = get_session().execute(query, {"id": theme_id})
        return self._unpack_theme(result)

    def get_words(self, theme_id) -> []:
        query = """ SELECT w.id, w.word FROM word w
                    RIGHT JOIN (
                        SELECT * FROM word_theme WHERE theme_id = :theme_id
                    ) as wt
                    ON w.id = wt.word_id"""
        result = get_session().execute(query, {"theme_id": theme_id} )
        return self._unpack_words(result)

    def get_all_words(self) -> []:
        query = """ SELECT id, word FROM word"""
        result = get_session().execute(query)
        return self._unpack_words(result)

    def remove_word_from_theme(self, theme_id, word_id):
        query = "DELETE FROM word_theme WHERE theme_id=:theme_id AND word_id=:word_id"
        get_session().execute( query, {"word_id": word_id, "theme_id": theme_id} )
        get_session().commit()

    def add_word_to_theme(self, theme_id, word_id):
        query = "INSERT INTO word_theme VALUES ( DEFAULT, :word_id, :theme_id )"
        get_session().execute( query, {"word_id": word_id, "theme_id": theme_id} )
        get_session().commit()

    def add_words(self, word_list, theme_ids):
        for word in word_list:
            query1 = "INSERT INTO word VALUES ( DEFAULT, :word ) ON CONFLICT DO NOTHING"
            get_session().execute( query1, {"word": word} )
            for theme_id in theme_ids:
                query2 = """ INSERT INTO word_theme VALUES (
                    DEFAULT,
                    ( SELECT id FROM word WHERE word=:word ),
                    :theme_id
                )  ON CONFLICT DO NOTHING """
                get_session().execute( query2, {"word": word, "theme_id": theme_id} )
        get_session().commit()
    
    def add_theme(self, theme_name):
        query = "INSERT INTO theme VALUES ( DEFAULT, :theme_name )"
        get_session().execute( query, {"theme_name": theme_name} )
        get_session().commit()
        
    def remove_theme(self, theme_id):
        query1 = "DELETE FROM word_theme WHERE theme_id=:theme_id"
        query2 = "DELETE FROM game_result WHERE theme_id=:theme_id"
        query3 = "DELETE FROM theme WHERE id=:theme_id"

        get_session().execute( query1, {"theme_id": theme_id} )
        get_session().execute( query2, {"theme_id": theme_id} )
        get_session().execute( query3, {"theme_id": theme_id} )
        get_session().commit()

        
    def remove_word(self, word_id):
        query1 = "DELETE FROM word_theme WHERE word_id=:word_id"
        query2 = "DELETE FROM word WHERE id=:word_id"

        get_session().execute( query1, {"word_id": word_id} )
        get_session().execute( query2, {"word_id": word_id} )
        get_session().commit()
        
    def remove_words(self, word_ids):
        for word_id in word_ids:
            query1 = "DELETE FROM word_theme WHERE word_id=:word_id"
            query2 = "DELETE FROM word WHERE id=:word_id"

            get_session().execute( query1, {"word_id": word_id} )
            get_session().execute( query2, {"word_id": word_id} )

        get_session().commit()

    def add_result(self, account_id : int, theme_id : int, score : int):
        query = "INSERT INTO game_result VALUES ( DEFAULT, :account_id, :theme_id, :score )"
        get_session().execute( query, {"account_id": account_id, "theme_id": theme_id, "score": score} )
        get_session().commit()

    def add_account(self, username : str, password : str, is_admin : bool):
        query = "INSERT INTO account VALUES ( DEFAULT, :username, :password, :is_admin )"
        get_session().execute( query, {"username": username, "password": password, "is_admin": is_admin} )
        get_session().commit()

    def get_account_by_username(self, username : str):
        query = "SELECT * FROM account WHERE username=:username"
        result = get_session().execute( query, {"username": username} )
        return self._unpack_account(result)

    def get_account(self, id : int):
        query = "SELECT * FROM account WHERE id=:id"
        result = get_session().execute( query, {"id": id} )
        return self._unpack_account(result)

    def get_top_results(self, theme_id : int, result_count : int):
        query = """SELECT ROW_NUMBER() OVER (ORDER BY r.score DESC) position, r.*, a.username FROM game_result r 
                    LEFT JOIN account a ON r.account_id = a.id 
                    WHERE r.theme_id = :theme_id
                    ORDER BY r.score DESC
                    LIMIT :result_count"""
        result = get_session().execute( query, {"theme_id": theme_id, "result_count": result_count} )
        return self._unpack_results(result)



