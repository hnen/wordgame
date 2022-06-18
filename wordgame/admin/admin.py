from ..auth import AuthSession
from ..db import Dao, Theme
import re

def is_user_admin():
    auth = AuthSession()
    dao = Dao()

    if not auth.is_logged_in():
        return False

    acc_id = auth.get_account()
    acc = dao.get_account(acc_id)

    if not acc or not acc.is_admin:
        return False

    return True

def add_words(word_list, theme_ids):
    dao = Dao()

    accepted, rejected = validate_words(word_list)

    print("ACCEPTED: ", str(accepted))
    print("REJECTED: ", str(rejected))
    print("theme ids: ", str(theme_ids))

    dao.add_words( accepted, theme_ids )

    return accepted, rejected
    
def validate_word(word):
    length = len(word)
    if length < 3 or length > 8:
        return False

    if re.search( "[^a-zåäö]", word ):
        return False

    return True

def validate_theme(theme):
    length = len(theme)
    if length < 3 or length > 32:
        return False

    if re.search( "[^a-zåäöA-ZÅÄÖ0-9 !?,]", theme ):
        return False

    return True


def validate_words(word_list):
    rejected = []
    accepted = []
    for word in word_list:
        if validate_word(word):
            accepted.append(word)
        else:
            rejected.append(word)
    return (accepted, rejected)

