from requests import get
from json import loads

def get_random_quote():
    response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    return ('{quoteText} - {quoteAuthor}'.format(**loads(response.text)))
