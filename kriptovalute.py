import modeli
from bottle import *

@get('/')
def glavniMenu():
    return template('glavni.html')

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/oseba/<id>')
def oOsebi(id):
    racuni = modeli.id_st(mail)
    return template('oseba.html', emso = emso, racuni = racuni)

@get('/isci')
def isci():
    priimek = request.query.iskalniNiz
    rezultat = modeli.poisciPriimek(priimek)
    return template('isci.html', rezultat = rezultat)

@get('/registracija')
def glavni():
    return template('registriraj.html', ime = None, priimek = None, mail = None, napaka=None, geslo = None)

@post('/registracija')
def dodaj():
    ime = request.forms.ime
    priimek = request.forms.priimek
    mail = request.forms.mail
    geslo = request.forms.geslo
    return template('registriraj.html', ime = ime, priimek = priimek, mail = mail, geslo = None)
    redirect('/oseba/<id>')

@get('/prijava')
def glavni_p():
    mail = request.forms.mail
    geslo = request.forms.geslo
    return template('prijava.html', mail = mail, napaka=None, geslo = geslo)
    redirect('/oseba/<id>')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)

