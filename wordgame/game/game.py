from ..db import Dao, Word
from .session import Session
import time

GAME_DURATION_S = 302 # 2 seconds added as a 'buffer', it feels a bit nicer when timer stays one second at start time and one second at 00:00

def get_time_left():
    game_session = Session()
    return GAME_DURATION_S * 1000 - (time.time_ns() - game_session.get_start_time()) / 1_000_000;

def points_for_guess(guess_num : int):
    point_table = [10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    return point_table[min(guess_num, len(point_table) - 1)]

def is_correct(result):
    return all( r == "CORRECT" for r in result )

def evaluate_guess(guess : str, word : str):
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
    
