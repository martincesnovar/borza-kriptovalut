import sqlite3, os
IME_BAZE='Kriptovalute.db'

def ustvari_bazo(ime_baze):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(ime_baze)
    except Error as e:
        pass
    finally:
        conn.close()

def sestavi_bazo(ime_baze=IME_BAZE,brisi=False):
    try:
        con = sqlite3.connect(ime_baze)
        cur = con.cursor()
        if brisi and os.path.exists(ime_baze):
            os.remove(ime_baze)
        ustvari_bazo(ime_baze)
        dodaj_osebo(ime_baze)
        dodaj_valute(ime_baze)
        dodaj_lastnistvo_valut(ime_baze)
        dodaj_zgodovino(ime_baze)
    except Exception as e:
        raise e
    finally:
        con.close()
    return True
    


def dodaj_osebo(ime_baze):
    con = sqlite3.connect(ime_baze)
    cur = con.cursor()
    sql = '''CREATE TABLE Oseba (
        id      INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL
                        UNIQUE,
        ime     CHAR    NOT NULL,
        priimek CHAR    NOT NULL,
        mail    CHAR    NOT NULL
                        UNIQUE,
        geslo   CHAR    NOT NULL
    );'''
    cur.execute(sql)


def dodaj_valute(ime_baze):
    con = sqlite3.connect(ime_baze)
    cur = con.cursor()
    sql='''CREATE TABLE Valuta (
    id  CHAR PRIMARY KEY 
                NOT NULL
                UNIQUE,
    ime CHAR    NOT NULL
    );'''
    cur.execute(sql)


def dodaj_zgodovino(ime_baze):
    con = sqlite3.connect(ime_baze)
    cur = con.cursor()
    sql = '''CREATE TABLE Zgodovina (
    Oseba    INTEGER  REFERENCES Oseba (id) 
                      NOT NULL,
    Valuta   CHAR     REFERENCES Valuta (id) 
                      NOT NULL,
    kolicina DECIMAL  NOT NULL,
    cena     DECIMAL  NOT NULL,
    datum    DATETIME DEFAULT (datetime('now') ) 
                      NOT NULL
    );'''
    cur.execute(sql)

def dodaj_lastnistvo_valut(ime_baze):
    con = sqlite3.connect(ime_baze)
    cur = con.cursor()
    sql = '''CREATE TABLE lastnistvo_valut (
    lastnik  INTEGER  REFERENCES Oseba (id) 
                      NOT NULL,
    valuta   CHAR  NOT NULL
                      REFERENCES Valuta (id),
    vrednost DECIMAL  NOT NULL,
    kolicina DECIMAL  NOT NULL,
    Datum    DATETIME NOT NULL
                      DEFAULT (datetime('now') ) 
    );'''
    cur.execute(sql)

