import sqlite3
import datetime
con = sqlite3.connect('Kriptovalute.db')

###########################################################################
#                                                                         #
#                           OSEBNI PODATKI LASTNIKA                       #
#                                                                         #
###########################################################################

def ime(id_st):
    '''funckija vrne ime lastnika z id_st-jem id'''
    sql = '''SELECT ime
            FROM osebe
            WHERE id = ?'''
    for ime in con.execute(sql,[id_st]):
        return ime[0]

def priimek(id_st):
    '''funckija vrne priimek lastnika z id-jem id'''
    sql = '''SELECT priimek
            FROM osebe
            WHERE id = ?'''
    for priimek in con.execute(sql,[id_st]):
        return priimek[0]

def id_je_v_bazi(id):
    '''Funkcija vrne True ali False glede na to, če id je v bazi'''
    sql = '''SELECT id FROM osebe'''
    sezID = []
    for idVBazi in con.execute(sql):
        sezID.append(idVBazi[0])
    # pogledamo če id je v bazi
    return id in set(sezID)


def poisci_lastnika(ime, priimek):
    ''' funkcija poisce lastnike, ki imajo skupne podatke ime, priimek'''
    sql =''' SELECT id, ime, priimek, FROM osebe WHERE ime LIKE ? AND priimek LIKE ? '''
    sezOseb = []
    for a, i,p in con.execute(sql, ['%'+ime+'%', '%'+priimek+'%']):
        sezOseb.append([a, i, p])
    return sezOseb
        

###########################################################################
#                                                                         #
#                           DODAJANJE V BAZO                              #
#                                                                         #
###########################################################################

def dodaj_lastnika_kriptovalute(ime, priimek):
    '''funkcija doda novega lastnika in sicer osnovne podatke'''
    sql = ''' INSERT INTO osebe (ime, priimek)
              VALUES (?,?)'''
    leto = int(datum_rojstva.split('/')[2])
    danes = int(str(datetime.datetime.now()).split('-')[0])
    con.execute(sql, [ime, priimek, datum_rojstva, spol, celica])
    con.commit()



def kupi_valuto(lastnik, valuta, vrednost, datum = datetime.datetime.now()):
    ''' funkcija doda kriptovaluto lastniku'''
    sql2 = '''INSERT INTO lastnistvo_valut (lastnik, valuta, vrednost, Datum)
              VALUES (?,?,?,?)'''
    con.execute(sql2,[lastnik, valuta, vrednost, datum])
    con.commit()




###########################################################################
#                                                                         #
#                           POMOŽNE FUNKCIJE                              #
#                                                                         #
###########################################################################







    
