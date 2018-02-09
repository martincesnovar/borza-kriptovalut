import modeli, dobi_zneske
from bottle import *
import hashlib # racunaje md5

secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"

def get_administrator():
    username = request.get_cookie('administrator', secret=secret)
    return username

    
def get_user(auto_login = True):
    """Poglej cookie in ugotovi, kdo je prijavljeni uporabnik,
       vrni njegov username in ime. Če ni prijavljen, presumeri
       na stran za prijavo ali vrni None (advisno od auto_login).
    """
    # Dobimo username iz piškotka
    username = request.get_cookie('username', secret=secret)
    # Preverimo, ali ta uporabnik obstaja
    if username is not None:
        r = modeli.mail(username)
        if r is not None:
            # uporabnik obstaja, vrnemo njegove podatke
            return r
    # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect, če ni administratorjevega coockie-ja
    if auto_login and not get_administrator():
        redirect('/prijava')
    else:
        return None

def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

@get('/')
def glavniMenu():
    return template('glavni.html')

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/oseba/<id_st>')
def oOsebi(id_st):
    mail=get_user()
    admin = get_administrator()
    uporabnik = modeli.podatki(id_st)
    vsota = 0
    if admin or (uporabnik is not None and mail[0] == uporabnik[3]):
        id, ime, priimek, mail, geslo = uporabnik
        valute = modeli.seznam_valut()
        lastnistvo = modeli.vsi_podatki(id_st)
        for _, _ , _, nova_vrednost, kol, _ in lastnistvo:
            vsota+=nova_vrednost*kol
        vsota = round(vsota,2)
        zasluzek = modeli.zasluzek(id)
        return template('oseba.html', id=id, ime = ime, priimek=priimek, mail=mail,valute=valute,kolicina=None,lastnistvo=lastnistvo, zasluzek=zasluzek, vsota=vsota)
    abort(401, 'Nimate pravic za ogled strani')


@post('/kupi')
def nakup():
    mail = get_user()
    admin = get_administrator()
    id = request.forms.id
    ime = request.forms.k
    vrednost = request.forms.vrednost
    kolicina = request.forms.kolicina
    modeli.kupi_valuto(id, ime, vrednost, kolicina)
    redirect('/oseba/'+str(id))
    return template('oseba.html', id=id, ime = ime, kolicina=kolicina,vrednost=vrednost,k=k)

@post('/prodaj')
def prodaj():
    mail = get_user()
    admin = get_administrator()
    id = request.forms.id
    ime = request.forms.valut
    vred = request.forms.vredn
    kol = float(request.forms.kol)
    kolicina = float(request.forms.kolicina)
    kolicina = min(kol, kolicina)
    modeli.prodaj_valuto(id, ime, kolicina,vred)
    redirect('/oseba/'+str(id))
    return template('oseba.html', id=id, ime = ime, kol=kol,vred=vred,kolicina=kolicina)

@get('/administrator')
def administrator():
    if get_administrator():
        return template('administrator.html')
    abort(401, 'Nimate pravic za ogled strani')

@get('/administrator/osebe')
def administrator_osebe():
    if get_administrator():
        sez = {}
        rezultat = modeli.podatki_vsi()
        for el in rezultat:
            sez[el[0]]=modeli.zasluzek(el[0])
        return template('seznam_oseb.html', rezultat=rezultat,zasluzek=sez)
    abort(401, 'Nimate pravic za ogled strani')

@get('/administrator/valute')
def administrator_valute():
    if get_administrator():
        rezultat = modeli.seznam_valut()
        return template('seznam_valut.html', rezultat=rezultat)
    abort(401, 'Nimate pravic za ogled strani')

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
    geslo = password_md5(request.forms.geslo)
    if ime and priimek and mail and geslo:
        je_v_bazi = modeli.mail_v_bazi(mail)
        if je_v_bazi or mail=="admin@admin":
            redirect('/registracija')
            return template('registriraj.html', ime=None, priimek=None, mail=None, geslo=None, napaka = 'Uporabnik obstaja')
        modeli.dodaj_osebo(ime, priimek, mail, geslo)
        id_1 = modeli.id_st(mail)
        response.set_cookie('username', mail, path='/', secret=secret)
        redirect('/oseba/'+str(id_1))
        return template('registriraj.html', ime = ime, priimek = priimek, mail = mail, geslo = geslo, napaka=None)
    redirect('/registracija')
    return template('registriraj.html', ime=None, priimek=None, mail=None, geslo=None, napaka = 'Neveljavna registracija')

@get('/oseba/<id>/spremeni')
def spremen(id):
    return template('spremeni.html', ime = None, priimek = None, mail = get_user()[0], staro_geslo = None, geslo = None, napaka=None)

@post('/spremeni')
def spremeni():
    mail = get_user()[0]
    id = modeli.id_st(mail)
    ime = request.forms.ime or modeli.ime(id)
    priimek = request.forms.priimek or modeli.priimek(id)
    staro_geslo = request.forms.staro_geslo
    geslo = password_md5(request.forms.geslo)
    if password_md5(staro_geslo) == modeli.geslo(id):
        modeli.spremeni_osebo(id, ime, priimek, mail, geslo)
    modeli.spremeni_osebo(id, ime, priimek, mail, modeli.geslo(id))
    response.set_cookie('username', mail, path='/', secret=secret)
    redirect('/oseba/'+str(id))
    return template('spremeni.html', ime = ime, priimek = priimek, staro_geslo = staro_geslo, mail = mail, geslo = geslo, napaka=None)
    

@get('/prijava')
def glavni():
    return template('prijava.html', mail = None, napaka=None, geslo = None)


@post('/prijava')
def glavni_p():
    mail = request.forms.mail
    geslo = password_md5(request.forms.geslo)
    if mail == "admin@admin" and geslo == password_md5("admin"):
        response.set_cookie('administrator', mail, path='/', secret=secret)
        redirect('/administrator')
        return template('prijava.html', mail = mail, napaka=None, geslo = geslo)
    id_s = modeli.id_st(mail)
    podatki = modeli.podatki(id_s)
    if podatki is not None:
        _, _, _, email, psw = podatki
        if email == mail and geslo == psw:
            response.set_cookie('username', mail, path='/', secret=secret)
            redirect('/oseba/'+str(id_s))
            return template('prijava.html', mail = mail, napaka=None, geslo = geslo)
        else:
            return template('prijava.html', mail=None, geslo=None, napaka='Neveljavna prijava')
    else:

        return template('prijava.html', mail = None, geslo = None, napaka = 'Izpolni polja')

@get('/zapri_racun')
def odstrani_g():
    return template('zapri_racun.html',mail=None,geslo=None,napaka=None)

@post('/zapri_racun')
def odstrani():
    mail = request.forms.mail
    geslo = password_md5(request.forms.geslo)
    id = modeli.id_st(mail)
    podatki = modeli.podatki(id)
    if podatki is not None:
        id_s, _, _, email, psw = podatki
        if email == mail and geslo == psw and id==id_s:
            modeli.zapri_racun(id)
            redirect('/')
            return template('zapri_racun.html', mail=mail, geslo=geslo,napaka=None)
        redirect('/zapri_racun')
        return template('zapri_racun.html', mail=mail, geslo=geslo, napaka='Nepravilno mail/geslo')
    return template('zapri_racun.html', mail=None, geslo=None, napaka=None)


@get('/dodaj_valute')
def dodaj_valute():
    if get_administrator():
        rezultat = modeli.seznam_valut()
        redirect('/administrator/valute')
        return template('seznam_valut.html', rezultat=rezultat)

@post('/dodaj_valute')
def dodaj_valute():
    if get_administrator():
        modeli.dodaj_valute()
        rezultat = modeli.seznam_valut()
        redirect('/administrator/valute')
        return template('seznam_valut.html', rezultat=rezultat)

@get('/dodaj_nove_valute')
def dodaj_valute():
    if get_administrator():
        rezultat = modeli.seznam_valut()
        redirect('/administrator/valute')
        return template('seznam_valut.html', rezultat=rezultat)

@post('/dodaj_nove_valute')
def dodaj_nove_valute():
    if get_administrator():
        modeli.dodaj_nove_valute()
        rezultat = modeli.seznam_valut()
        redirect('/administrator/valute')
        return template('seznam_valut.html', rezultat=rezultat)

@get('/oseba/<id>/zgodovina')
def zgodovina(id):
    mail = get_user()
    uporabnik = modeli.podatki(id)
    if get_administrator() or uporabnik is not None and mail[0] == uporabnik[3]:
        zgodovina_transakcij = modeli.vrni_zgodovino(id)
        zasluzek = modeli.zasluzek(id)
        return template('zgodovina.html',zasluzek=zasluzek,lastnistvo=zgodovina_transakcij)
    else:
        odjava()

@get('/odjavi')
def odjava():
    response.delete_cookie('username')
    redirect('/')

@get('/odjava')
def odjavi():
    response.delete_cookie('administrator')
    redirect('/')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080,debug=True, reloader=True) #problem reloader idle
