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
    racuni = None
    return template('oseba.html', racuni = racuni)

@get('/isci')
def isci():
    priimek = request.query.iskalniNiz
    rezultat = modeli.poisciPriimek(priimek)
    return template('isci.html', rezultat = rezultat)

@get('/registracija')
def glavni():
    return template('registriraj.html', ime = None, priimek = None, mail = None, napaka=None, geslo = None)

@get('/registracija')
def dodaj():
    ime = request.forms.ime
    priimek = request.forms.priimek
    mail = request.forms.mail
    geslo = request.forms.geslo
    modeli.dodaj_osebo(ime, priimek, mail, geslo)
    id_1 = modeli.id_st(mail)
    redirect('/oseba/'+str(id_1))
    return template('registriraj.html', ime = ime, priimek = priimek, mail = mail, geslo = geslo, napaka=None)

@get('/prijava')
def glavni():
    return template('prijava.html', mail = None, napaka=None, geslo = None)
    

@post('/prijava')
def glavni_p():
    mail = request.forms.mail
    geslo = request.forms.geslo
    id_s = modeli.id_st(mail)

    podatki =modeli.podatki(id_s)
    if podatki is not None:
        _, _, _, email, psw = podatki
        if email == mail and geslo == psw:
            redirect('/oseba/'+str(id_s))
            return template('prijava.html', mail = mail, napaka=None, geslo = geslo)
        else:
            return template('prijava.html', mail=None, geslo=None, napaka='Neveljavna prijava')
    else:
        return template('prijava.html', mail = None, geslo = None, napaka = 'Neveljavna prijava')


# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080,debug=True, reloader=True) #problem reloader idle
