import sqlite3, os
IME_BAZE='Kriptovalute.db'
con = sqlite3.connect(IME_BAZE)
cur = con.cursor()

def sestavi_bazo(ime_baze=IME_BAZE,brisi=False):
    if brisi and os.path.exists(ime_baze):
        os.remove(ime_baze)
    dodaj_osebo()
    dodaj_valute()
    dodaj_lastnistvo_valut()
    dodaj_zgodovino()


def dodaj_osebo():
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


def dodaj_valute():
    sql='''CREATE TABLE Valuta (
    id  INTEGER PRIMARY KEY AUTOINCREMENT
                NOT NULL
                UNIQUE,
    ime         NOT NULL
                UNIQUE
    );'''
    cur.execute(sql)


def dodaj_zgodovino():
    sql = '''CREATE TABLE Zgodovina (
    Oseba             REFERENCES Oseba (id) 
                      NOT NULL,
    Valuta            REFERENCES Valuta (id) 
                      NOT NULL,
    Datum    DATETIME DEFAULT (datetime('now') ) 
                      NOT NULL,
    kolicina INTEGER
    );'''
    cur.execute(sql)

def dodaj_lastnistvo_valut():
    sql = '''CREATE TABLE lastnistvo_valut (
    lastnik  INTEGER  REFERENCES Oseba (id) 
                      NOT NULL,
    valuta   INTEGER  NOT NULL
                      UNIQUE
                      REFERENCES Valuta (id),
    vrednost DECIMAL  NOT NULL,
    kolicina INTEGER  NOT NULL,
    Datum    DATETIME NOT NULL
                      DEFAULT (datetime('now') ) 
    );'''
    cur.execute(sql)

