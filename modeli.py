import sqlite3
import datetime
import dobi_zneske
con = sqlite3.connect('Kriptovalute.db')
cur = con.cursor()

###########################################################################
#                                                                         #
#                           OSEBNI PODATKI LASTNIKA                       #
#                                                                         #
###########################################################################

def podatki_vsi():
    '''funckija vrne vse lastnike'''
    sql = '''SELECT * FROM oseba'''
    cur = con.execute(sql)
    return cur.fetchall()

def podatki(id_st):
    '''funckija vrne ime lastnika z id_st-jem id'''
    sql = '''SELECT *
            FROM oseba
            WHERE id = ?'''
    for pod in con.execute(sql,[id_st]):
        return pod

def ime(id_st):
    '''funckija vrne ime lastnika z id_st-jem id'''
    sql = '''SELECT ime
            FROM oseba
            WHERE id = ?'''
    for ime in con.execute(sql,[id_st]):
        return ime[0]

def priimek(id_st):
    '''funckija vrne priimek lastnika z id-jem id'''
    sql = '''SELECT priimek
            FROM oseba
            WHERE id = ?'''
    for priimek in con.execute(sql,[id_st]):
        return priimek[0]

def id_st(mail):
    '''funckija vrne id lastnika z mailom
    za prijavo preko maila.'''
    sql = '''SELECT id
            FROM oseba
            WHERE mail = ?'''
    for id_s in con.execute(sql,[mail]):
        return id_s[0]

def id_je_v_bazi(id):
    '''Funkcija vrne True ali False glede na to, če id je v bazi'''
    sql = '''SELECT id FROM oseba'''
    sezID = []
    for idVBazi in con.execute(sql):
        sezID.append(idVBazi[0])
    # pogledamo če id je v bazi
    return id in set(sezID)


def poisci_osebo(ime, priimek):
    ''' funkcija poisce lastnike, ki imajo skupne podatke ime, priimek'''
    sql =''' SELECT id, ime, priimek, mail, stanje FROM oseba WHERE ime LIKE ? AND priimek LIKE ? '''
    sezOseb = []
    for id, ime, priimek, mail, geslo in con.execute(sql, ['%'+ime+'%', '%'+priimek+'%']):
        sezOseb.append([id, ime, priimek, mail, geslo])
    return sezOseb

def dolzniki():
    ''' funkcija vrne lastnike, ki dolgujejo denar'''
    sql =''' SELECT id, ime, priimek, mail, stanje FROM oseba
    WHERE stanje < 0'''
    sezOseb = []
    for id, ime, priimek, mail, stanje in con.execute(sql):
        sezOseb.append([id, ime, priimek, mail, stanje])
    return sezOseb

def seznam_valut():
    sql = '''SELECT * FROM Valuta'''
    sez = []
    podatki = dobi_zneske.vrni_podatke()
    for k, ime in con.execute(sql):
        spletna = dobi_zneske.generiraj_spletno(ime.lower())
        vrednost, evri, cas = podatki.get(ime.lower(),(0,0,0))
        if (vrednost, cas) != (0, 0):
            sez.append((k, ime, spletna, vrednost, evri, dobi_zneske.datum(cas)))
    return sez

def ime_valute(id):
    sql = '''SELECT ime FROM Valuta
    WHERE id = (?)'''
    for ime in con.execute(sql,[id]):
        return ime[0]

def kupljene_valute(id):
    sql = '''SELECT valuta, vrednost,
    SUM(kolicina) as kolicina, max(Datum) as datum FROM lastnistvo_valut
    WHERE (SELECT id FROM Oseba
    WHERE lastnistvo_valut.lastnik = (?))
    GROUP BY valuta'''
    sez = []
    for valuta, vrednost, kolicina, datum in con.execute(sql,[id]):
        sez.append((valuta, ime_valute(valuta), vrednost, kolicina, datum))
    return sez


def zasluzek(id):
    sql='''SELECT -SUM(kolicina* cena)
    FROM Zgodovina WHERE (?) = Oseba
    GROUP BY Oseba, Valuta'''
    sez = []
    for vrednost, in con.execute(sql,[id]):
        sez.append(vrednost)
    return round(sum(sez),2)

def vrni_zgodovino(id):
    '''[id, valuta, kolicina, cena, datum]'''
    sez = []
    sql='''SELECT * FROM Zgodovina WHERE
Zgodovina.Oseba = (?)'''
    for el in con.execute(sql, [id]):
        sez.append(el)
    return sez
    

###########################################################################
#                                                                         #
#                           DODAJANJE V BAZO                              #
#                                                                         #
###########################################################################

def dodaj_osebo(ime, priimek, mail, geslo):
    '''funkcija doda novega lastnika in sicer osnovne podatke'''
    sql = ''' INSERT INTO oseba (ime, priimek, mail, geslo)
              VALUES (?,?,?,?)'''
    con.execute(sql, [ime, priimek, mail, geslo])
    con.commit()

def dodaj_v_zgodovino(lastnik, valuta, kolicina, cena, datum = datetime.datetime.now()):
    sql = '''INSERT INTO Zgodovina (Oseba, Valuta, kolicina, cena)
            VALUES (?,?,?,?)'''
    con.execute(sql,[lastnik, valuta, kolicina, cena])
    con.commit()

def kupi_valuto(lastnik, valuta, vrednost, kolicina, datum = datetime.datetime.now()):
    sql = '''INSERT INTO lastnistvo_valut (lastnik, valuta, vrednost, kolicina)
              VALUES (?,?,?,?)'''
    dodaj_v_zgodovino(int(lastnik), valuta, float(kolicina), float(vrednost),datum)
    con.execute(sql,[int(lastnik), valuta, float(vrednost), float(kolicina)])
    con.commit()


def _dodaj_valute():
    ''' funkcija doda kriptovaluto v bazo'''
    sql = '''INSERT INTO Valuta (id, ime)
              VALUES (?,?)'''
    napaka = None
    try:
        for kratica, ime, _ in dobi_zneske.imena_valut('https://bittrex.com/api/v1.1/public/getcurrencies'):
            con.execute(sql,[kratica, ime])
    except Exception as e:
        napaka = e
    finally:
        con.commit()
    return napaka

def dodaj_valute():
    sql = '''DELETE FROM Valuta'''
    a = _dodaj_valute()
    if a:
        con.execute(sql)
        con.commit()
    _dodaj_valute()
        
    


###########################################################################
#                                                                         #
#                           ODSTRANJEVANJE IZ BAZE                        #
#                                                                         #
###########################################################################

def prodaj_valuto(lastnik, valuta, kolicina,cena,vse=False):
    sql_1 = '''SELECT kolicina FROM lastnistvo_valut
    WHERE (SELECT id FROM oseba WHERE (SELECT id FROM Valuta
          WHERE (?) = lastnistvo_valut.lastnik AND (?) = lastnistvo_valut.valuta))'''
    for kol in con.execute(sql_1,[lastnik, valuta]):
        dodaj_v_zgodovino(lastnik,valuta,-float(kolicina),cena)
        prodaj = max(kol[0]-float(kolicina),0)
        if vse or prodaj==0:
            sql = '''DELETE FROM lastnistvo_valut 
                  WHERE (SELECT id FROM oseba WHERE (SELECT id FROM Valuta
                  WHERE (?) = lastnistvo_valut.lastnik AND (?) = lastnistvo_valut.valuta))'''
            con.execute(sql,[int(lastnik), valuta])
        else:
            sql = '''UPDATE lastnistvo_valut
              SET kolicina = (?), Datum = datetime('now')
              WHERE (SELECT id FROM oseba WHERE (SELECT id FROM Valuta
              WHERE (?) = lastnistvo_valut.lastnik AND (?) = lastnistvo_valut.valuta))'''
            con.execute(sql,[prodaj, int(lastnik), valuta])  
        con.commit()


def zbrisi_zgodovino(lastnik):
    sql = '''DELETE FROM Zgodovina
              WHERE (?) = Oseba'''
    con.execute(sql,[lastnik])
    con.commit()


def _zbrisi_osebo(id_osebe):
    ''' funkcija odstrani osebo'''
    sql = '''DELETE FROM oseba
    WHERE oseba.id = (?)'''
    con.execute(sql,[id_osebe])
    con.commit()

def zapri_racun(id_osebe):
    '''proda vse kriptovalute in zbriše osebo'''
    sql = '''SELECT * FROM lastnistvo_valut
    WHERE lastnik = (?)'''
    for id_o, id_valute, vrednost, kolicina, _ in con.execute(sql,[id_osebe]):
        zbrisi_zgodovino(int(id_osebe))
        prodaj_valuto(int(id_osebe), id_valute, kolicina,0.0,True)
    _zbrisi_osebo(id_osebe)


###########################################################################
#                                                                         #
#                           POSODABLJANJE BAZE                            #
#                                                                         #
###########################################################################

def spremeni_osebo(id, ime, priimek, mail, geslo):
    sql = ''' UPDATE oseba
                SET ime = (?), priimek = (?), mail = (?), geslo = (?)
              WHERE id = (?)'''
    con.execute(sql, [ime, priimek, mail, geslo, id])
    con.commit()    

###########################################################################
#                                                                         #
#                           POMOŽNE FUNKCIJE                              #
#                                                                         #
###########################################################################

def vsi_podatki(id_st):
    sez = []
    valute = seznam_valut()
    lastnistvo = kupljene_valute(id_st)
    for el in valute:
        kratica,ime,stran,vrednost_t,evri,datum=el
        for el in lastnistvo:
            kra,ime1,vrednost,kolicina,datum1=el
            if kratica == kra:
                sez.append((kra, ime, vrednost, vrednost_t, kolicina, datum1))
    return sez
                
