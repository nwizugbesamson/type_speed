import requests

URL = "https://random-word-api.herokuapp.com/word"

class Words:
    """generate random words from api
    retuns in string format
    """
    def __init__(self):
        self.current_words = ""


    def generate_words(self, lenght):
        params = {
            "number": lenght
        }
        r = requests.get(url=URL, params=params)
        data = r.json()[:]
        self.current_words = " ".join(data)
        return self.current_words