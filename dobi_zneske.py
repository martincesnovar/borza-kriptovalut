import urllib.request, json, time

naslov = 'https://www.bitstamp.net/api/ticker_hour/'
valute = 'https://bittrex.com/api/v1.1/public/getcurrencies'

def dobi_podatke(stran):
    '''Dobi podatke iz spleta in jih pretvori v slovar'''
    with urllib.request.urlopen(stran) as url:
        podatki = json.loads(url.read().decode())
    cas = datum(podatki.get('timestamp'))
    podatki['datetime'] = cas
    return podatki

          
def datum(podatki):
    '''pretvori in vrne čas v obliki (leto, mesec, dan, ura, min, sek,_ ,_)'''
    if podatki is not None:
        return time.gmtime(int(podatki))[:]
    return time.gmtime()[:]
