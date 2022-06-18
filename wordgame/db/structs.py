
class WordTheme:
    word_id = -1
    theme_id = -1

    def __init__(self, theme_id : int, word_id : int):
        self.word_id = word_id
        self.theme_id = theme_id
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class Word:
    id = -1
    word = ""

    def __init__(self, word_id : int, word : str):
        self.id = word_id
        self.word = word

    def __repr__ (self):
        return f'Word: {self.id}; {self.word}'

class Theme:
    id = -1
    name = ""
    word_count = 0

    def __init__(self, theme_id : int, name : str, word_count : int):
        self.id = theme_id
        self.name = name
        self.word_count = word_count

class Account:
    id = -1
    username = ""
    password = ""
    is_admin = False
    def __init__(self, id : int, username : str, password : str, is_admin : bool):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

class Result:
    position = -1
    username = ""
    score = -1

    def __init__(self, position : int, username : str, score : int):
        self.position = position
        self.username = username
        self.score = score
