import sqlite3
import datetime
con = sqlite3.connect('Kriptovalute.db')

###########################################################################
#                                                                         #
#                           OSEBNI PODATKI LASTNIKA                       #
#                                                                         #
###########################################################################

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

def dodaj_valuto(ime):
    '''Doda valuto'''
    sql = '''INSERT INTO Valuta (ime)
    VALUES (?)'''
    con.execute(sql,[ime])
    con.commit()

def kupi_valuto(lastnik, valuta, vrednost, datum = datetime.datetime.now()):
    ''' funkcija doda kriptovaluto lastniku
    - kriptovaluta je že v tabeli'''
    sql = '''INSERT INTO lastnistvo_valut (lastnik, valuta, vrednost, Datum)
              VALUES (?,?,?,?)'''
    con.execute(sql,[lastnik, valuta, vrednost, datum])
    con.commit()
    _dodaj_stanje(lastnik, -vrednost)


###########################################################################
#                                                                         #
#                           ODSTRANJEVANJE IZ BAZE                        #
#                                                                         #
###########################################################################

def prodaj_valuto(lastnik, vrednost, datum = datetime.datetime.now()):
    ''' funkcija proda kriptovaluto lastniku'''
    sql = '''DELETE FROM lastnistvo_valut
            '''
    con.execute(sql)
    con.commit()
    _dodaj_stanje(lastnik, vrednost)

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

def _spremeni_stanje(id_osebe, stanje):
    '''spremeni stanje osebe'''
    sql = '''UPDATE oseba
    SET stanje = ?
    WHERE id = ?'''
    con.execute(sql,[stanje, id_osebe])
    con.commit()

def _dodaj_stanje(id_osebe, vrednost):
    '''popravi stanje na računu'''
    sql = '''SELECT * FROM oseba
    WHERE id = ?'''
    sql_u = '''UPDATE oseba
    SET stanje = ?
    WHERE id = ?'''
    for id_osebe, _, _, _, stanje in con.execute(sql,[id_osebe]):
        stanje += vrednost
    con.execute(sql_u,[stanje, id_osebe])
    con.commit()
        
    

###########################################################################
#                                                                         #
#                           POMOŽNE FUNKCIJE                              #
#                                                                         #
###########################################################################

