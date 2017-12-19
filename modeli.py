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

def kupljene_valute(id):
    sql = '''SELECT valuta, SUM(vrednost)/COUNT(vrednost), SUM(kolicina) as kolicina, max(Datum) as datum FROM lastnistvo_valut
    WHERE (SELECT id FROM Oseba
    WHERE lastnistvo_valut.lastnik = (?))
    GROUP BY valuta'''
    sez = []
    for valuta, vrednost, kolicina, datum in con.execute(sql,[id]):
        sez.append((valuta, vrednost, kolicina, datum))
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

def kupi_valuto(lastnik, valuta, vrednost, kolicina, datum = datetime.datetime.now()):
    sql = '''INSERT INTO lastnistvo_valut (lastnik, valuta, vrednost, kolicina, Datum)
              VALUES (?,?,?,?,?)'''
    con.execute(sql,[lastnik, valuta, vrednost, kolicina, datum])
    con.commit()

def dodaj_valute():
    ''' funkcija doda kriptovaluto v bazo'''
    sql = '''INSERT INTO Valuta (kratica, ime)
              VALUES (?,?)'''
    napaka = None
    try:
        for kratica, ime, in dobi_zneske.imena_valut('https://bittrex.com/api/v1.1/public/getcurrencies'):
            con.execute(sql,[kratica, ime])
    except Exception as e:
        napaka = e
    finally:
        con.commit()
    return napaka


###########################################################################
#                                                                         #
#                           ODSTRANJEVANJE IZ BAZE                        #
#                                                                         #
###########################################################################

def prodaj_valuto(lastnik, valuta, vrednost):
    sql = '''DELETE FROM lastnistvo_valut 
            WHERE lastnik = Oseba.id AND valuta = Valuta.id'''
    con.execute(sql,[lastnik, valuta])
    con.commit()

def zbrisi_osebo(id_osebe):
    ''' funkcija odstrani osebo'''
    sql = '''DELETE FROM oseba
    WHERE oseba.id = (?)
            '''
    con.execute(sql,[id_osebe])
    con.commit()

def zapri_racun(id_osebe):
    '''proda vse kriptovalute in zbriše osebo'''
    sql = '''SELECT * FROM lastnistvo_valut
    WHERE lastnik = ?'''
    for id_osebe, id_valute, vrednost, _ in con.execute(sql,[id_osebe]):
        prodaj_valuto(id_osebe, id_valute, vrednost)
    zbrisi_osebo(id_osebe)


###########################################################################
#                                                                         #
#                           POSODABLJANJE BAZE                            #
#                                                                         #
###########################################################################

    

###########################################################################
#                                                                         #
#                           POMOŽNE FUNKCIJE                              #
#                                                                         #
###########################################################################

