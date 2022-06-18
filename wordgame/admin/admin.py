from flask import Blueprint, request, redirect, url_for, abort
from flask import render_template, jsonify
from ..auth import AuthSession
from ..db import Dao, Theme
import re

def do_add(dao, form):
    print("Adding:", form)

    word_list = parse_words(form["word_list"])
    theme_ids = parse_theme_ids(form)
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

def parse_words(words_raw):
    w = words_raw.split("\n")
    w = map( str.strip, w )
    w = map( str.lower, w )
    return list( w )

def parse_theme_ids(form):
    ret = []
    for (key, value) in form.items():
        if value == "on":
            match = re.search( "theme_\d+", key )
            if match:
                ret.append(int(match.group()[6:]))
    return ret

def parse_selected_words(form):
    ret = []
    for (key, value) in form.items():
        match = re.search( "select_\d+", key )
        if match:
            ret.append(int(match.group()[7:]))
    return ret
