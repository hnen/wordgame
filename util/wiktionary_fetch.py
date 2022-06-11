import requests, json, sys, re, random

fetchlist = ["Luokka:Fysiikka"]

def fetch_category( category ):
    #print(category)
    url = f'https://fi.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmlimit=500&cmtitle={category}&cmprop=title'
    x = requests.get(url)
    p = json.loads(x.text)

    cmcont = p["continue"]["cmcontinue"] if "continue" in p else None

    words = [(lambda x: x["title"])(x) for x in p["query"]["categorymembers"]]
    def accept(word):
        if len(word) < 3 or len(word) > 8:
            return False

        #if re.search( "[^a-zåäö]", word ):
        #    return False

        #if random.random() > 0.01:
        #    return False

        return True

    def out(word):
        try:
            out = word.encode('utf-8').decode(sys.stdout.encoding)
            print(out)
        except UnicodeDecodeError:
            pass

    def handle(word):
        if word.startswith("Category:") or word.startswith("Luokka:"):
            fetchlist.append(word)
        elif accept(word):
            out(word)


    for word in words:
        handle(word)
            
    while cmcont:
        cont_url =  f'{url}&cmcontinue={cmcont}'
        x = requests.get(cont_url)
        p = json.loads(x.text)
        cmcont = p["continue"]["cmcontinue"] if "continue" in p else None
        words = [(lambda x: x["title"])(x) for x in p["query"]["categorymembers"]]
        for word in words:
            handle(word)

while len(fetchlist) > 0:
    fetch_category(fetchlist[0])
    fetchlist = fetchlist[1:]
