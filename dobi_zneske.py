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

def imena_valut(naslov='https://bittrex.com/api/v1.1/public/getcurrencies'):
    sez = dobi_podatke(naslov)['result']
    seznam_valut=[]
    for i in range(len(sez)):
        if sez[i]['IsActive']:
            ime = sez[i]['CurrencyLong']
            ime_k = sez[i]['Currency']
            seznam_valut.append((ime_k,ime))
    return seznam_valut

def vrednost_valut():
    vrednost_valute = dobi_podatke('https://www.bitstamp.net/api/ticker_hour/')
    trenutna_vrednost = vrednost_valute['last']
    valute = [('BitCoin', trenutna_vrednost)]
    return valute
