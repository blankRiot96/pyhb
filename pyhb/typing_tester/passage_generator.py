import requests
from typing import List, Union
import json


Passage = Union[List[str], str]


def get_words(n: int) -> Passage:
    """
    :param n: Number of words to be returned. 1000 > n > 0
    """

    # Most commonly used English words API
    url = "https://most-common-words.herokuapp.com/api/search?top="

    words = [requests.get(url + str(i)).json()['word'] for i in range(1, n+1)]
    return (words[0], words)[len(words) > 1]


def get_sentences(n: int) -> Passage:
    """
    :param n: Number of sentences to be returned.
    """

    # Random facts API
    url = "https://uselessfacts.jsph.pl/random.json?language=en"

    # requests.get() returns a response object for the API
    # .content is an attribute that holds the content received from the API
    # which is a bytes json string: b'{"text": "some very random fact"}'
    # json.loads() converts that text into a Python object
    # 'text' is the key which holds the value of the random fact
    sentences = [json.loads(requests.get(url).content)['text'] for _ in range(n)]
    

    return (sentences[0], sentences)[len(sentences) > 1]

