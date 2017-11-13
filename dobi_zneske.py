import urllib.request, json

naslovi = 'https://www.bitstamp.net/api/ticker_hour/'

def json_from_web(stran):
    '''Dobi podatke iz spleta in jih pretvori v slovar'''
    with urllib.request.urlopen(stran) as url:
        data = json.loads(url.read().decode())
        return data
            
