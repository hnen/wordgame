import time
from enum import Enum

from ..db import Dao, Word
from .session import Session
from ..auth import AuthSession

GAME_DURATION_S = 182     # 2 seconds added as a 'buffer'. UI will subtract one second from time. It feels a bit nicer when timer stays one second at start time and one second at 00:00, especially if there happens to be network lag.

class GuessResult(Enum):
    INVALID = 0,
    WRONG = 1,
    RIGHT = 2,
    GAME_OVER = 3

class Game:
    _current_word = None

    def start(self, theme_id):
        session = Session()
        dao = Dao()
        self._current_word = dao.select_random_word(theme_id)
        session.start(theme_id, self._current_word.id, time.time_ns())
    
    def guess(self, guess):
        game_session = Session()
        auth_session = AuthSession()
        dao = Dao()

        if not game_session.is_active():
            return GuessResult.INVALID, None

        if self.get_time_left() <= 0:
            final_points = game_session.get_points()
            if final_points > 0:
                dao.add_result(auth_session.get_account(), game_session.get_theme_id(), final_points)
            game_session.expire()
            return GuessResult.GAME_OVER, None

        word_obj = self.get_current_word()

        if len(guess) != len(word_obj.word):
            return GuessResult.INVALID, None;

        result = self.evaluate_guess( guess, word_obj.word )

        got_points = 0
        correct_points = 0

        if self.is_correct(result):
            theme_id = game_session.get_theme_id()
            word_obj = dao.select_random_word(theme_id)
            game_session.set_word_id( word_obj.id )
            self._current_word = word_obj
            got_points = self.points_for_guess( game_session.get_guess_count() )
            game_session.set_points( game_session.get_points() + got_points )
            game_session.set_guess_count(0)
            return GuessResult.RIGHT, result
        else:
            game_session.set_guess_count(game_session.get_guess_count() + 1)
            return GuessResult.WRONG, result


    def get_points_for_curr_guess(self):
        game_session = Session()
        return self.points_for_guess(game_session.get_guess_count())

    def get_points(self):
        game_session = Session()
        return game_session.get_points()

    def get_current_word(self):
        if not self._current_word:
            session = Session()
            if not session.is_active():
                return None
            dao = Dao()
            self._current_word = dao.get_word( session.get_word_id() )

        return self._current_word

    def get_time_left(self):
        game_session = Session()
        return GAME_DURATION_S * 1000 - (time.time_ns() - game_session.get_start_time()) / 1_000_000;

    def points_for_guess(self, guess_num : int):
        point_table = [10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        return point_table[min(guess_num, len(point_table) - 1)]

    def is_correct(self, result):
        return all( r == "CORRECT" for r in result )

    def evaluate_guess(self, guess : str, word : str):
        if len(guess) != len(word):
            return []

        result = [ "WRONG" ] * len(word)
        
        char_map = {}
        for c in range(ord('a'), ord('z') + 1):
            char_map[chr(c)] = 0
        char_map['ä'] = 0
        char_map['ö'] = 0
        char_map['å'] = 0

        for i in range(len(word)):
            word_c = word[i].lower()
            char_map[word_c] += 1

        # Check letters in right position
        for i in range(len(word)):
            word_c = word[i].lower()
            if word[i].lower() == guess[i].lower():
                char_map[word_c] -= 1
                result[i] = "CORRECT"

        # Check letters in wrong position
        for i in range(len(word)):
            word_c = word[i].lower()
            guess_c = guess[i].lower()
            if word[i].lower() != guess[i].lower() and char_map[guess_c] > 0:
                char_map[guess_c] -= 1
                result[i] = "HINT"

        return result
        
