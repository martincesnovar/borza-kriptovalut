import modeli, dobi_zneske
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
        valute = modeli.seznam_valut()
        lastnistvo = modeli.kupljene_valute(id_st)
        return template('oseba.html', id=id, ime = ime, priimek=priimek, mail=mail,valute=valute,kolicina=None,lastnistvo=lastnistvo)

@post('/kupi')
def nakup():
    id = request.forms.id
    ime = request.forms.ime
    vrednost = request.forms.vrednost
    kolicina = request.forms.kolicina
    modeli.kupi_valuto(id, ime, vrednost, kolicina)
    redirect('/oseba/'+str(id))
    return template('oseba.html', id=id, ime = ime, kolicina=kolicina,vrednost=vrednost)

@post('/prodaj')
def prodaj():
    redirect('/oseba/<id_st>')
    return

@get('/administrator/osebe')
def administrator_osebe():
    rezultat = modeli.podatki_vsi()
    return template('administrator.html', rezultat=rezultat)

@get('/administrator/valute')
def administrator_valute():
    rezultat = modeli.seznam_valut()
    return template('seznam_valut.html', rezultat=rezultat)

@get('/isci')
def isci():
    id_st = request.query.iskalniNiz
    rezultat = modeli.podatki(id_st)
    if rezultat is not None:
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


@get('/zapri_racun')
def odstrani_g():
    return template('zapri_racun.html',mail=None,geslo=None,napaka=None)

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
        redirect('/zapri_racun')
        return template('zapri_racun.html', mail=mail, geslo=geslo, napaka='Nepravilno mail/geslo')
    return template('zapri_racun.html', mail=None, geslo=None, napaka=None)

@post('/dodaj_valute')
def dodaj_valute():
    modeli.dodaj_valute()
    rezultat = modeli.seznam_valut()
    return template('seznam_valut.html', rezultat=rezultat)

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080,debug=True, reloader=True) #problem reloader idle
