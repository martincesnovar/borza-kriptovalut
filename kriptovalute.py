import modeli
from bottle import *

@get('/')
def glavniMenu():
    return template('glavni.html')

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/oseba/<id_st>')
def oOsebi(id_st):
    if modeli.podatki(id_st) is not None:
        id, ime, priimek, mail, geslo = modeli.podatki(id_st)
        return template('oseba.html', id=id, ime = ime, priimek=priimek, mail=mail)

@get('/isci')
def isci():
    priimek = request.query.iskalniNiz
    rezultat = modeli.poisciPriimek(priimek)
    return template('isci.html', rezultat = rezultat)

@get('/registracija')
def glavni_r():
    return template('registriraj.html', ime = None, priimek = None, mail = None, napaka=None, geslo = None)

@post('/registracija')
def dodaj():
    ime = request.forms.ime
    priimek = request.forms.priimek
    mail = request.forms.mail
    geslo = request.forms.geslo
    if ime and priimek and mail and geslo:
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


@post('/zapri_racun')
def odstrani():
    mail = request.forms.mail
    geslo = request.forms.geslo
    id = modeli.id_st(mail)
    podatki = modeli.podatki(id)
    if podatki is not None:
        id_s, _, _, email, psw = podatki
        if email == mail and geslo == psw and id==id_s:
            modeli.zbrisi_osebo(id)
            redirect('/')
            return template('zapri_racun.html', mail=mail, geslo=geslo,napaka=None)
        return template('zapri_racun.html', mail=mail, geslo=geslo, napaka='Nepravilno mail/geslo')
    return template('zapri_racun.html', mail=mail, geslo=geslo, napaka=None)



# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080,debug=True, reloader=True) #problem reloader idle
