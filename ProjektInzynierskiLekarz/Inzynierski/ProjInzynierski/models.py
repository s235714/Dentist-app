from datetime import datetime
from ProjInzynierski import db
from pony.orm import *
from datetime import date
from flask_login import UserMixin, LoginManager

class Osoba(db.Entity):
    osoba_id = PrimaryKey(int, auto=True)
    imie1 = Required(str)
    imie2 = Optional(str, nullable=True)
    nazwisko = Required(str)
    pesel = Required(str, unique=True)
    data_ur = Optional(str, nullable=True)
    plec = Required(str)
    email = Optional(str, nullable=True)
    adresadres_id = Optional("Adres")
    telefontelefon_id = Optional("Telefon")
    gabinetgabinet_id = Optional("Gabinet")
    logowanie = Optional("Logowanie")
    pacjent = Optional("Pacjent")
    lekarz = Optional("Lekarz")

class Logowanie(db.Entity, UserMixin):
    dane_log_id = PrimaryKey(int, auto=True)
    rodzaj_konta = Required(int)
    login = Required(str)
    haslo = Required(str)
    osobaosoba_id = Required("Osoba")

    def get_id(self):
        return self.dane_log_id

class Lekarz(db.Entity):
    lekarz_id = PrimaryKey(int, auto=True)
    numer_licen = Optional(str, nullable=True)
    data_upr = Optional(str, nullable=True)
    specjalizacje = Optional(str, nullable=True)
    osobaosoba_id = Required("Osoba")
    doktor = Set("Pacjent")
    recepty = Set("Recepta")
    zabiegi = Set("Zabieg")

class Pacjent(db.Entity):
    pacjent_id = PrimaryKey(int, auto=True)
    nr_karty = Required(str, unique=True)
    higiena = Optional(str, nullable=True)
    zgryz = Optional(str, nullable=True)
    blona_sluzowa = Optional(str, nullable=True)
    uzup_protet = Optional(LongStr, nullable=True)
    przyzebie = Optional(LongStr, nullable=True)
    choroby = Optional(LongStr, nullable=True)
    leki = Optional(LongStr, nullable=True)
    uczulenia = Optional(LongStr, nullable=True)
    czy_dziecko = Optional(str, nullable=True)
    lekarzlekarz_id = Required("Lekarz")
    osobaosoba_id = Required("Osoba")
    zabiegi = Set("Zabieg")
    uzebienie = Set("Uzebienie")
    recepty = Set("Recepta")

class Adres(db.Entity):
    adres_id = PrimaryKey(int, auto=True)
    wojewodztwo = Optional(str, nullable=True)
    gmina = Optional(str, nullable=True)
    miejscowosc = Required(str)
    ulica = Optional(str, nullable=True)
    nr_domu = Required(str)
    nr_lokalu = Optional(str, nullable=True)
    kod_poczt = Required(str)
    osoba = Set("Osoba")
    gabinet = Set("Gabinet")  

class Telefon(db.Entity):
    telefon_id = PrimaryKey(int, auto=True)
    czy_telefon = Required(int)
    telefon_kom1 = Optional(str, nullable=True)
    telefon_kom2 = Optional(str, nullable=True)
    telefon_kom3 = Optional(str, nullable=True)
    telefon_stacj = Optional(str, nullable=True)
    telefon_stacj2 = Optional(str, nullable=True)
    telefon_zagr = Optional(str, nullable=True)
    telefon_zagr2 = Optional(str, nullable=True)
    osoba = Set("Osoba")
    gabinet = Set("Gabinet")

class Gabinet(db.Entity):
    gabinet_id = PrimaryKey(int, auto=True)
    nazwa = Required(str)
    regon = Optional(str, nullable=True)
    nip = Optional(str, nullable=True)
    adresadres_id = Optional("Adres")
    telefontelefon_id = Optional("Telefon")
    osoba = Set("Osoba")
    recepty = Set("Recepta")

class Recepta(db.Entity):
    recepta_id = PrimaryKey(int, auto=True)
    nr_recepty = Optional(str, unique=True, nullable=True)
    oddz_NFZ = Required(str)
    upraw_dod = Optional(str, nullable=True)
    odplatnosc = Optional(str, nullable=True)
    przep_leki = Required(LongStr)
    data_wyst = Required(str)
    data_realiz = Optional(str, nullable=True)
    lekarzlekarz_id = Required("Lekarz")
    zabiegzabieg_id = Optional(int, nullable=True)
    pacjentpacjent_id = Required("Pacjent")
    gabinetgabinet_id = Optional("Gabinet")

class Zabieg(db.Entity):
    zabieg_id = PrimaryKey(int, auto=True)
    data_zabiegu = Required(str)
    zab = Optional(str, nullable=True)
    opis_zabiegu = Required(LongStr)
    kod_uslugi_ICD10 = Optional(str, nullable=True)
    kod_procedury_ICD9 = Optional(str, nullable=True)
    ilosc = Optional(str, nullable=True)
    mat_kolor = Optional(str, nullable=True)
    lekarzlekarz_id = Required("Lekarz")
    pacjentpacjent_id = Required("Pacjent")

class Uzebienie(db.Entity):
    uzebienie_id = PrimaryKey(int, auto=True)
    zab = Optional(str, nullable=True)
    stan_zeba = Optional(str, nullable=True)
    data_pocz = Optional(str, nullable=True)
    data_kon = Optional(str, nullable=True)
    pacjentpacjent_id = Required("Pacjent")

