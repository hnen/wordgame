import requests, json, sys, re, random

url = "https://fi.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmlimit=500&cmtitle=Category:Suomen_kielen_substantiivit&cmprop=title"
x = requests.get(url)
p = json.loads(x.text)

cmcont = p["continue"]["cmcontinue"] if "continue" in p else None

words = [(lambda x: x["title"])(x) for x in p["query"]["categorymembers"]]

def accept(word):
    if len(word) < 4 or len(word) > 8:
        return False

    if re.search( "[^a-zåäö]", word ):
        return False

    if random.random() > 0.1:
        return False

    return True

def out(word):
    try:
        out = word.encode('utf-8').decode(sys.stdout.encoding)
        print(out)
    except UnicodeDecodeError:
        pass

for word in words:
    if accept(word):
        out(word)
        
while cmcont:
    cont_url =  f'{url}&cmcontinue={cmcont}'
    x = requests.get(cont_url)
    p = json.loads(x.text)
    cmcont = p["continue"]["cmcontinue"] if "continue" in p else None
    words = [(lambda x: x["title"])(x) for x in p["query"]["categorymembers"]]
    for word in words:
        if accept(word):
            out(word)
