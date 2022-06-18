from flask import session

class Session:
    KEY_WORD_ID = "game_word_id"
    KEY_THEME_ID = "game_theme_id"
    KEY_START_TIME = "game_start_time"
    KEY_GUESS_COUNT = "game_guess_count"
    KEY_POINTS = "game_points"

    def is_active(self):
        return (self.KEY_WORD_ID in session) and session[self.KEY_WORD_ID] > 0

    def get_word_id(self):
        if self.is_active():
            return session[self.KEY_WORD_ID]
        return -1

    def set_word_id(self, id : int):
        session[self.KEY_WORD_ID] = id

    def set_theme_id(self, id : int):
        session[self.KEY_THEME_ID] = id

    def set_guess_count(self, cnt : int):
        session[self.KEY_GUESS_COUNT] = cnt

    def set_points(self, points : int):
        session[self.KEY_POINTS] = points

    def get_theme_id(self):
        return session[self.KEY_THEME_ID]

    def get_guess_count(self):
        return session[self.KEY_GUESS_COUNT]

    def get_points(self):
        return session[self.KEY_POINTS]

    def set_start_time(self, time : int):
        session[self.KEY_START_TIME] = time

    def get_start_time(self):
        return int(session[self.KEY_START_TIME])

    def start(self, theme_id, word_id, start_time):
        self.set_theme_id(theme_id)
        self.set_word_id(word_id)
        self.set_start_time(start_time)
        self.set_guess_count(0)
        self.set_points(0)

    def expire(self):
        session.pop(self.KEY_WORD_ID, None)
        session.pop(self.KEY_THEME_ID, None)
        session.pop(self.KEY_START_TIME, None)