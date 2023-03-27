import os
from flask import render_template, url_for, flash, redirect
from ProjInzynierski import app
from ProjInzynierski.forms import *
from pony.orm import *
from ProjInzynierski.models import *
from flask_bcrypt import Bcrypt
from flask_login import current_user, logout_user, login_user, login_required
import datetime

bcrypt=Bcrypt()
db.bind(provider='mysql', host='localhost', user='root', passwd='', db='GabinetStomatologiczny')
set_sql_debug(True)     #wyswietla w konsoli jakie zapytania sql wykonal
db.generate_mapping(create_tables=True) #tworzy tablice jesli nie istnialy na podstawie class Nazwa(db.Entity)

@db_session
def add_rejestracjaosoba(imie1,imie2,nazwisko,pesel,data_ur,plec,email):
    Osoba(imie1=imie1,imie2=imie2,nazwisko=nazwisko,pesel=pesel,data_ur=data_ur,plec=plec,email=email)

@db_session
def add_rejestracjanowegopacjenta(imie1,imie2,nazwisko,pesel,data_ur,plec,email):
    return Osoba(imie1=imie1,imie2=imie2,nazwisko=nazwisko,pesel=pesel,data_ur=data_ur,plec=plec,email=email)

@db_session
def add_logindoosoby(login,haslo,id_osoby):
    Logowanie(rodzaj_konta=2,login=login,haslo=haslo,osobaosoba_id=id_osoby)

@db_session
def add_logindonowegopacjenta(login,haslo,id_osoby):
    Logowanie(rodzaj_konta=1,login=login,haslo=haslo,osobaosoba_id=id_osoby)

@db_session
def add_nowylekarz(numer_licen,data_upr,specjalizacje,osobaosoba_id):
    Lekarz(numer_licen=numer_licen,data_upr=data_upr,specjalizacje=specjalizacje,osobaosoba_id=osobaosoba_id)

@db_session
def add_nowypacjent(nr_karty,higiena,zgryz,blona_sluzowa,uzup_protet,przyzebie,choroby,leki,uczulenia,czy_dziecko,lekarzlekarz_id,osobaosoba_id):
    Pacjent(nr_karty=nr_karty,higiena=higiena,zgryz=zgryz,blona_sluzowa=blona_sluzowa,uzup_protet=uzup_protet,przyzebie=przyzebie,choroby=choroby,leki=leki,uczulenia=uczulenia,czy_dziecko=czy_dziecko,lekarzlekarz_id=lekarzlekarz_id,osobaosoba_id=osobaosoba_id)

@db_session
def add_nowyadres(wojewodztwo,gmina,miejscowosc,ulica,nr_domu,nr_lokalu,kod_poczt):
    return Adres(wojewodztwo=wojewodztwo,gmina=gmina,miejscowosc=miejscowosc,ulica=ulica,nr_domu=nr_domu,nr_lokalu=nr_lokalu,kod_poczt=kod_poczt)      

@db_session
def add_nowyadresdogabinetu(miejscowosc,ulica,nr_domu,nr_lokalu,kod_poczt):
    return Adres(miejscowosc=miejscowosc,ulica=ulica,nr_domu=nr_domu,nr_lokalu=nr_lokalu,kod_poczt=kod_poczt) 

@db_session
def add_nowytelefon(telefon_kom1,telefon_kom2,telefon_kom3,telefon_stacj,telefon_stacj2,telefon_zagr,telefon_zagr2):
    return Telefon(czy_telefon=1,telefon_kom1=telefon_kom1,telefon_kom2=telefon_kom2,telefon_kom3=telefon_kom3,telefon_stacj=telefon_stacj,telefon_stacj2=telefon_stacj2,telefon_zagr=telefon_zagr,telefon_zagr2=telefon_zagr2)

@db_session
def add_nowytelefondopacjenta(telefon_kom1,telefon_kom2,telefon_kom3,telefon_stacj,telefon_stacj2,telefon_zagr,telefon_zagr2):
    return Telefon(czy_telefon=1,telefon_kom1=telefon_kom1,telefon_kom2=telefon_kom2,telefon_kom3=telefon_kom3,telefon_stacj=telefon_stacj,telefon_stacj2=telefon_stacj2,telefon_zagr=telefon_zagr,telefon_zagr2=telefon_zagr2)

@db_session
def add_nowygabinet(nazwa,regon,nip):
    return Gabinet(nazwa=nazwa,regon=regon,nip=nip)

@db_session
def add_nowarecepta(nr_recepty,oddz_NFZ,upraw_dod,odplatnosc,przep_leki,data_wyst,data_realiz,lekarzlekarz_id,pacjentpacjent_id,gabinetgabinet_id):
    Recepta(nr_recepty=nr_recepty,oddz_NFZ=oddz_NFZ,upraw_dod=upraw_dod,odplatnosc=odplatnosc,przep_leki=przep_leki,data_wyst=data_wyst,data_realiz=data_realiz,lekarzlekarz_id=lekarzlekarz_id,pacjentpacjent_id=pacjentpacjent_id,gabinetgabinet_id=gabinetgabinet_id)

@db_session
def add_nowyzabieg(data_zabiegu,zab,opis_zabiegu,kod_uslugi_ICD10,kod_procedury_ICD9,ilosc,mat_kolor,lekarzlekarz_id,pacjentpacjent_id):
    Zabieg(data_zabiegu=data_zabiegu,zab=zab,opis_zabiegu=opis_zabiegu,kod_uslugi_ICD10=kod_uslugi_ICD10,kod_procedury_ICD9=kod_procedury_ICD9,ilosc=ilosc,mat_kolor=mat_kolor,lekarzlekarz_id=lekarzlekarz_id,pacjentpacjent_id=pacjentpacjent_id)

@db_session
def add_uzebieniepacjenta(zab,stan_zeba,data_pocz,data_kon,pacjentpacjent_id):
    Uzebienie(zab=zab,stan_zeba=stan_zeba,data_pocz=data_pocz,data_kon=data_kon, pacjentpacjent_id=pacjentpacjent_id)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Utworzono konto dla użytkownika {form.name.data} {form.last_name.data}!', 'success')
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        add_rejestracjaosoba(form.name.data,form.second_name.data,form.last_name.data,form.pesel.data,form.data_ur.data,form.plec.data,form.email.data)
        dodanaosoba=db.Osoba.get(pesel=form.pesel.data)
        add_logindoosoby(form.username.data,hashed_password,dodanaosoba)
        return redirect(url_for('login'))
    return render_template('register.html', title='Zarejestruj się', form=form)

@app.route("/addNewPatient", methods=['GET', 'POST'])
def addNewPatient():
    dodanaosoba = []
    form = AddNewPatientForm()
    if form.validate_on_submit():
        flash(f'Dodano nowego pacjenta {form.name.data} {form.last_name.data}!', 'success')
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        dodanaosoba = add_rejestracjanowegopacjenta(form.name.data,form.second_name.data,form.last_name.data,form.pesel.data,form.data_ur.data,form.plec.data,form.email.data)
        dodanaosoba.flush()
        add_logindonowegopacjenta(form.username.data,hashed_password,dodanaosoba)
        dodanaosoba.gabinetgabinet_id=1
        return redirect(url_for('accountPatient', osoba_id=dodanaosoba.osoba_id))
    return render_template('addNewPatient.html', title='Dodawanie danych osobowych nowego pacjenta', form=form, dodanaosoba=dodanaosoba)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        possible_user = db.Logowanie.get(login=form.username.data)
        if not possible_user:
            flash('Nie udało się zalogować, niepoprawny login lub hasło!', 'danger')
            return redirect(url_for('login'))
        if bcrypt.check_password_hash(possible_user.haslo, form.password.data):
            login_user(possible_user)
            if current_user.rodzaj_konta==2:
                return redirect(url_for('accountDoctor'))            
            else:
                flash('Nieznany typ konta!', 'danger')
        else:
            flash('Nie udało się zalogować, niepoprawny login lub hasło!', 'danger')
    return render_template('login.html', title='Zaloguj się', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/modifyLoginData/<int:osoba_id>", methods=['GET', 'POST'])
def modifyLoginData(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    dane_logowania = Logowanie[osoba_id]
    form = ModifyLoginForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(dane_logowania.haslo, form.password.data):
            hashed_password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            dane_logowania.haslo = hashed_password
            flash('Poprawna edycja hasła dostępu!', 'success')
            return redirect(url_for('accountDoctor'))                
    return render_template('modifyLoginData.html', form=form, title='Edycja danych logowania', buttontext='Edycja danych logowania')

@app.route("/accountDoctor", methods=['GET', 'POST'])
def accountDoctor():
    doktor = db.Osoba.get(osoba_id=current_user.osoba_id)
    return render_template('accountDoctor.html', title='Konto lekarza', doktor=doktor)

@app.route("/accountPatient<int:osoba_id>")
def accountPatient(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    return render_template('accountPatient.html', title='Konto pacjenta', pacjent=pacjent)

@app.route("/addDoctor", methods=['GET', 'POST'])
def addDoctor():
    doktor = db.Osoba.get(osoba_id=current_user.osoba_id)
    form = DoctorForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano informacje o lekarzu!', 'success')
        add_nowylekarz(form.licence_number.data,form.date_upr.data,form.specjalizacje.data,doktor.osoba_id)
        return redirect(url_for('manageDoctor', osoba_id=current_user.osoba_id))
    return render_template('addDoctor.html', title='Dodawanie informacji o lekarzu', form=form, doktor=doktor)

@app.route("/manageDoctor<int:osoba_id>", methods=['GET', 'POST'])
def manageDoctor(osoba_id):
    lekarz = db.Lekarz.get(osobaosoba_id=current_user.osoba_id)
    if not lekarz:
        flash(f'Dodaj dodatkowe informacje o lekarzu!', 'warning')
        lekarz = []  
    return render_template('manageDoctor.html', title='Zarządzanie informacjami o lekarzu', lekarz=lekarz)

@app.route("/modifyDoctor", methods=['GET', 'POST'])
def modifyDoctor():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    lekarz = db.Lekarz.get(osobaosoba_id=current_user.osoba_id)
    form = ModifyDoctorForm()
    if form.validate_on_submit():
        lekarz.numer_licen = form.licence_number.data
        lekarz.data_upr = form.date_upr.data
        lekarz.specjalizacje = form.specjalizacje.data
        flash('Poprawna edycja informacji o lekarzu!', 'success')
        return redirect(url_for('manageDoctor', osoba_id=current_user.osoba_id))

    form.licence_number.data = lekarz.numer_licen
    form.date_upr.data = lekarz.data_upr
    form.specjalizacje.data = lekarz.specjalizacje   
    return render_template('modifyDoctor.html', title='Edycja informacji o lekarzu', form=form, osoba=osoba, lekarz=lekarz)

@app.route("/addHealthCondition<int:osoba_id>", methods=['GET', 'POST'])
def addHealthCondition(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    doktor = db.Osoba.get(osoba_id=current_user.osoba_id)
    form = PatientForm()
    if doktor.lekarz:
        form = PatientForm()
        if form.validate_on_submit():
            flash(f'Poprawnie dodano informacje o stanie zdrowia i jamy ustnej!', 'success')
            add_nowypacjent(form.card_number.data,form.higiena.data,form.zgryz.data,form.blona_sluzowa.data,form.uzup_protet.data,form.przyzebie.data,form.choroby.data,form.leki.data,form.uczulenia.data,form.czy_dziecko.data,doktor.lekarz.lekarz_id,osoba.osoba_id)
            return redirect(url_for('manageHealthCondition', osoba_id=osoba_id))
    else:
        flash(f'Aby dodać informacje o stanie zdrowia pacjenta, najpierw dodaj informacje dodatkowe o lekarzu!', 'warning')    
    return render_template('addHealthCondition.html', title='Dodawanie informacji o stanie zdrowia', form=form, osoba=osoba, doktor=doktor)

@app.route("/manageHealthCondition<int:osoba_id>", methods=['GET', 'POST'])
def manageHealthCondition(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    stanzdrowia = db.Pacjent.get(osobaosoba_id=osoba_id)
    if not stanzdrowia:
        flash(f'Dodaj informacje o stanie zdrowia i jamy ustnej!', 'warning')
        stanzdrowia = []
    return render_template('manageHealthCondition.html', title='Zarządzanie informacjami o stanie zdrowia', osoba=osoba, stanzdrowia=stanzdrowia)

@app.route("/modifyHealthCondition/<int:pacjent_id>/<int:osoba_id>", methods=['GET', 'POST'])
def modifyHealthCondition(pacjent_id,osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    stanzdrowia = db.Pacjent.get(osobaosoba_id=osoba_id)
    form = ModifyPatientForm()
    if form.validate_on_submit():
        stanzdrowia.nr_karty = form.card_number.data
        stanzdrowia.higiena = form.higiena.data
        stanzdrowia.zgryz = form.zgryz.data
        stanzdrowia.blona_sluzowa = form.blona_sluzowa.data
        stanzdrowia.uzup_protet = form.uzup_protet.data
        stanzdrowia.przyzebie = form.przyzebie.data
        stanzdrowia.choroby = form.choroby.data
        stanzdrowia.leki = form.leki.data
        stanzdrowia.uczulenia = form.uczulenia.data
        stanzdrowia.czy_dziecko = form.czy_dziecko.data
        flash('Poprawna edycja informacji o stanie zdrowia pacjenta!', 'success')
        return redirect(url_for('manageHealthCondition', osoba_id=osoba_id))

    form.card_number.data = stanzdrowia.nr_karty
    form.higiena.data = stanzdrowia.higiena
    form.zgryz.data = stanzdrowia.zgryz
    form.blona_sluzowa.data = stanzdrowia.blona_sluzowa
    form.uzup_protet.data = stanzdrowia.uzup_protet
    form.przyzebie.data = stanzdrowia.przyzebie
    form.choroby.data = stanzdrowia.choroby
    form.leki.data = stanzdrowia.leki
    form.uczulenia.data = stanzdrowia.uczulenia
    form.czy_dziecko.data = stanzdrowia.czy_dziecko              
    return render_template('modifyHealthCondition.html', title='Edytowanie informacji o stanie zdrowia', form=form, osoba=osoba, stanzdrowia=stanzdrowia)

@app.route("/addPatientAddress<int:osoba_id>", methods=['GET', 'POST'])
def addPatientAddress(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    form = AddressForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano adres zamieszkania!', 'success')
        adres = add_nowyadres(form.wojewodztwo.data,form.gmina.data,form.miejscowosc.data,form.ulica.data,form.nr_domu.data,form.nr_lokalu.data,form.kod_poczt.data)
        adres.flush()
        pacjent.adresadres_id = adres.adres_id
        return redirect(url_for('managePatientPersonalData', osoba_id=osoba_id))
    return render_template('addPatientAddress.html', title='Dodawanie adresu zamieszkania pacjenta', form=form, pacjent=pacjent)    

@app.route("/addOfficeAddress", methods=['GET', 'POST'])
def addOfficeAddress():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    adresdogabinetu = gabinet.adresadres_id
    form = OfficeAddressForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano adres gabinetu!', 'success')
        dodanyadres = add_nowyadresdogabinetu(form.miejscowosc.data,form.ulica.data,form.nr_domu.data,form.nr_lokalu.data,form.kod_poczt.data)
        dodanyadres.flush()
        gabinet.adresadres_id = dodanyadres.adres_id
        return redirect(url_for('manageOffice', osoba_id=current_user.osoba_id))
    return render_template('addOfficeAddress.html', title='Dodawanie adresu gabinetu', form=form, osoba=osoba, gabinet=gabinet, adresdogabinetu=adresdogabinetu)

@app.route("/modifyPatientAddress<int:osoba_id>", methods=['GET', 'POST'])
def modifyPatientAddress(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    adres = pacjent.adresadres_id
    form = ModifyAddressForm()
    if form.validate_on_submit():
        adres.wojewodztwo = form.wojewodztwo.data
        adres.gmina = form.gmina.data
        adres.miejscowosc = form.miejscowosc.data
        adres.ulica = form.ulica.data
        adres.nr_domu = form.nr_domu.data
        adres.nr_lokalu = form.nr_lokalu.data
        adres.kod_poczt = form.kod_poczt.data
        flash('Poprawna edycja adresu zamieszkania!', 'success')
        return redirect(url_for('managePatientPersonalData', osoba_id=osoba_id))

    form.wojewodztwo.data = adres.wojewodztwo
    form.gmina.data = adres.gmina
    form.miejscowosc.data = adres.miejscowosc
    form.ulica.data = adres.ulica
    form.nr_domu.data = adres.nr_domu
    form.nr_lokalu.data = adres.nr_lokalu
    form.kod_poczt.data = adres.kod_poczt
    return render_template('modifyPatientAddress.html', form=form, title='Edycja adresu zamieszkania', pacjent=pacjent, adres=adres)

@app.route("/modifyOfficeAddress", methods=['GET', 'POST'])
def modifyOfficeAddress():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    adresdogabinetu = gabinet.adresadres_id
    form = ModifyOfficeAddressForm()
    if form.validate_on_submit():
        adresdogabinetu.miejscowosc = form.miejscowosc.data
        adresdogabinetu.ulica = form.ulica.data
        adresdogabinetu.nr_domu = form.nr_domu.data
        adresdogabinetu.nr_lokalu = form.nr_lokalu.data
        adresdogabinetu.kod_poczt = form.kod_poczt.data
        flash('Poprawna edycja adresu gabinetu!', 'success')
        return redirect(url_for('manageOffice', osoba_id=current_user.osoba_id))

    form.miejscowosc.data = adresdogabinetu.miejscowosc
    form.ulica.data = adresdogabinetu.ulica
    form.nr_domu.data = adresdogabinetu.nr_domu
    form.nr_lokalu.data = adresdogabinetu.nr_lokalu
    form.kod_poczt.data = adresdogabinetu.kod_poczt
    return render_template('modifyOfficeAddress.html', title='Edycja adresu gabinetu', form=form, osoba=osoba, gabinet=gabinet, adresdogabinetu=adresdogabinetu)

@app.route("/addPatientTelephone<int:osoba_id>", methods=['GET', 'POST'])
def addPatientTelephone(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    form = TelephoneForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano telefon kontaktowy!', 'success')
        dodanytelefon = add_nowytelefondopacjenta(form.telefon_kom1.data,form.telefon_kom2.data,form.telefon_kom3.data,form.telefon_stacj.data,form.telefon_stacj2.data,form.telefon_zagr.data,form.telefon_zagr2.data)
        dodanytelefon.flush()
        pacjent.telefontelefon_id = dodanytelefon.telefon_id
        return redirect(url_for('managePatientPersonalData', osoba_id=osoba_id)) 
    return render_template('addPatientTelephone.html', title='Dodawanie telefonu kontaktowego', form=form, pacjent=pacjent)

@app.route("/addOfficeTelephone", methods=['GET', 'POST'])
def AddOfficeTelephone():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    telefondogabinetu = gabinet.telefontelefon_id
    form = TelephoneForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano telefon do gabinetu!', 'success')
        dodanytelefon = add_nowytelefon(form.telefon_kom1.data,form.telefon_kom2.data,form.telefon_kom3.data,form.telefon_stacj.data,form.telefon_stacj2.data,form.telefon_zagr.data,form.telefon_zagr2.data)
        dodanytelefon.flush()
        gabinet.telefontelefon_id = dodanytelefon.telefon_id
        return redirect(url_for('manageOffice', osoba_id=current_user.osoba_id))  
    return render_template('addOfficeTelephone.html', title='Dodawanie telefonu do gabinetu', form=form, osoba=osoba, gabinet=gabinet, telefondogabinetu=telefondogabinetu)

@app.route("/modifyPatientTelephone<int:osoba_id>", methods=['GET', 'POST'])
def modifyPatientTelephone(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    telefon = pacjent.telefontelefon_id
    form = ModifyTelephoneForm()
    if form.validate_on_submit():
        telefon.telefon_kom1 = form.telefon_kom1.data
        telefon.telefon_kom2 = form.telefon_kom2.data
        telefon.telefon_kom3 = form.telefon_kom3.data
        telefon.telefon_stacj = form.telefon_stacj.data
        telefon.telefon_stacj2 = form.telefon_stacj2.data
        telefon.telefon_zagr = form.telefon_zagr.data
        telefon.telefon_zagr2 = form.telefon_zagr2.data
        flash('Poprawna edycja telefonu kontaktowego!', 'success')
        return redirect(url_for('managePatientPersonalData', osoba_id=osoba_id))

    form.telefon_kom1.data = telefon.telefon_kom1
    form.telefon_kom2.data = telefon.telefon_kom2
    form.telefon_kom3.data = telefon.telefon_kom3
    form.telefon_stacj.data = telefon.telefon_stacj
    form.telefon_stacj2.data = telefon.telefon_stacj2
    form.telefon_zagr.data = telefon.telefon_zagr
    form.telefon_zagr2.data = telefon.telefon_zagr2
    return render_template('modifyPatientTelephone.html', title='Edycja telefonu kontaktowego', form=form, pacjent=pacjent, telefon=telefon)

@app.route("/modifyOfficeTelephone", methods=['GET', 'POST'])
def modifyOfficeTelephone():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    telefondogabinetu = gabinet.telefontelefon_id
    form = ModifyTelephoneForm()
    if form.validate_on_submit():
        telefondogabinetu.telefon_kom1 = form.telefon_kom1.data
        telefondogabinetu.telefon_kom2 = form.telefon_kom2.data
        telefondogabinetu.telefon_kom3 = form.telefon_kom3.data
        telefondogabinetu.telefon_stacj = form.telefon_stacj.data
        telefondogabinetu.telefon_stacj2 = form.telefon_stacj2.data
        telefondogabinetu.telefon_zagr = form.telefon_zagr.data
        telefondogabinetu.telefon_zagr2 = form.telefon_zagr2.data
        flash('Poprawna edycja telefonu do gabinetu!', 'success')
        return redirect(url_for('manageOffice', osoba_id=current_user.osoba_id))

    form.telefon_kom1.data = telefondogabinetu.telefon_kom1
    form.telefon_kom2.data = telefondogabinetu.telefon_kom2
    form.telefon_kom3.data = telefondogabinetu.telefon_kom3
    form.telefon_stacj.data = telefondogabinetu.telefon_stacj
    form.telefon_stacj2.data = telefondogabinetu.telefon_stacj2
    form.telefon_zagr.data = telefondogabinetu.telefon_zagr
    form.telefon_zagr2.data = telefondogabinetu.telefon_zagr2  
    return render_template('modifyOfficeTelephone.html', title='Edycja telefonu do gabinetu', form=form, osoba=osoba, gabinet=gabinet, telefondogabinetu=telefondogabinetu)

@app.route("/addOffice", methods=['GET', 'POST'])
def addOffice():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    form = OfficeForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano informacje o gabinecie!', 'success')
        dodanygabinet = add_nowygabinet(form.nazwa.data,form.regon.data,form.nip.data)
        dodanygabinet.flush()
        osoba.gabinetgabinet_id = dodanygabinet.gabinet_id
        return redirect(url_for('manageOffice', osoba_id=current_user.osoba_id))
    return render_template('addOffice.html', title='Dodawanie informacji o gabinecie', osoba=osoba, form=form)

@app.route("/manageOffice<int:osoba_id>")
def manageOffice(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    adresdogabinetu = []
    telefondogabinetu = []
    if not gabinet:
        flash('Dodaj informacje o gabinecie!', 'warning')
    else:
        gabinet = osoba.gabinetgabinet_id
        adresdogabinetu = gabinet.adresadres_id
        telefondogabinetu = gabinet.telefontelefon_id
    return render_template('manageOffice.html', title='Zarządzanie gabinetem', osoba=osoba, gabinet=gabinet, adresdogabinetu=adresdogabinetu, telefondogabinetu=telefondogabinetu)

@app.route("/modifyOffice", methods=['GET', 'POST'])
def modifyOffice():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    form = ModifyOfficeForm()
    if form.validate_on_submit():   #jesli wszystko zostalo wpisane odpowiednio
        gabinet.nazwa = form.nazwa.data
        gabinet.regon= form.regon.data
        gabinet.nip = form.nip.data
        flash('Poprawna edycja informacji o gabinecie!', 'success')
        return redirect(url_for('manageOffice', osoba_id=current_user.osoba_id))

    form.nazwa.data = gabinet.nazwa
    form.regon.data = gabinet.regon
    form.nip.data = gabinet.nip     
    return render_template('modifyOffice.html', title='Edycja informacji o gabinecie', form=form)

@app.route("/addPrescription<int:osoba_id>", methods=['GET', 'POST'])
def addPrescription(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    form = PrescriptionForm()
    if osoba.pacjent:
        form = PrescriptionForm()
        if form.validate_on_submit():
            if form.prescription_num.data:
                flash(f'Poprawnie dodano receptę o numerze "{form.prescription_num.data}"!', 'success')
            else:
                flash(f'Poprawnie dodano nową receptę!', 'success')
            add_nowarecepta(form.prescription_num.data,form.oddz_NFZ.data,form.upraw_dod.data,form.odplatnosc.data,form.przep_leki.data,form.data_wyst.data,form.data_realiz.data,osoba.pacjent.lekarzlekarz_id,osoba.pacjent.pacjent_id,osoba.gabinetgabinet_id)
            return redirect(url_for('managePrescriptions', osoba_id=osoba_id))
    else:
        flash(f'Aby dodać pierwszą receptę, najpierw dodaj informacje o stanie zdrowia pacjenta!', 'warning')    
    return render_template('addPrescription.html', title='Dodawanie informacji o recepcie', form=form, osoba=osoba)

@app.route("/managePrescriptions<int:osoba_id>", methods=['GET', 'POST'])
def managePrescriptions(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    if osoba.pacjent:
        recepty = osoba.pacjent.recepty
    else:
        flash(f'Dodaj pierwszą receptę dla pacjenta {osoba.imie1} {osoba.nazwisko}!', 'warning')
        recepty = [] 
    return render_template('managePrescriptions.html', title='Zarządzanie informacjami o receptach', osoba=osoba, recepty=recepty)

@app.route("/modifyPrescription/<int:recepta_id>/<int:osoba_id>", methods=['GET', 'POST'])
def modifyPrescription(recepta_id,osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    recepty = Recepta[recepta_id]
    form = ModifyPrescriptionForm()
    if form.validate_on_submit():
        recepty.nr_recepty = form.prescription_num.data
        recepty.oddz_NFZ = form.oddz_NFZ.data
        recepty.upraw_dod = form.upraw_dod.data
        recepty.odplatnosc = form.odplatnosc.data
        recepty.przep_leki = form.przep_leki.data
        recepty.data_wyst = form.data_wyst.data
        recepty.data_realiz = form.data_realiz.data
        flash('Poprawna edycja informacji o recepcie!', 'success')
        return redirect(url_for('managePrescriptions', osoba_id=osoba_id))

    form.prescription_num.data = recepty.nr_recepty
    form.oddz_NFZ.data = recepty.oddz_NFZ
    form.upraw_dod.data = recepty.upraw_dod
    form.odplatnosc.data = recepty.odplatnosc
    form.przep_leki.data = recepty.przep_leki
    form.data_wyst.data = recepty.data_wyst
    form.data_realiz.data = recepty.data_realiz 
    return render_template('modifyPrescription.html', title='Edycja informacji o recepcie', form=form, osoba=osoba, recepty=recepty)

@app.route("/addTeethCondition<int:osoba_id>", methods=['GET', 'POST'])
def addTeethCondition(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    form = TeethForm()
    if osoba.pacjent:
        form = TeethForm()
        if form.validate_on_submit():   #jesli wszystko zostalo wpisane odpowiednio
            flash(f'Poprawnie dodano informacje o zębie!', 'success')
            add_uzebieniepacjenta(form.zab.data,form.stan_zeba.data,form.data_pocz.data,form.data_kon.data,osoba.pacjent.pacjent_id)
            return redirect(url_for('manageTeethCondition', osoba_id=osoba_id))
    else:
        flash(f'Aby dodać pierwszą informację o stanie uzębienia pacjenta, najpierw dodaj informacje o stanie zdrowia pacjenta!', 'warning')    
    return render_template('addTeethCondition.html', title='Dodawanie informacji o stanie uzębienia', form=form, osoba=osoba)

@app.route("/manageTeethCondition<int:osoba_id>", methods=['GET', 'POST'])
def manageTeethCondition(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    if osoba.pacjent:
        uzebienie = osoba.pacjent.uzebienie
    else:
        flash(f'Dodaj pierwszą informację o stanie uzębienia pacjenta {osoba.imie1} {osoba.nazwisko}!', 'warning')
        uzebienie = [] 
    return render_template('manageTeethCondition.html', title='Zarządzanie informacjami o stanie uzębienia', osoba=osoba, uzebienie=uzebienie)    

@app.route("/modifyTeethCondition/<int:uzebienie_id>/<int:osoba_id>", methods=['GET', 'POST'])
def modifyTeethCondition(uzebienie_id, osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    uzebienie = Uzebienie[uzebienie_id]
    form = ModifyTeethForm()
    if form.validate_on_submit():
        uzebienie.zab = form.zab.data
        uzebienie.stan_zeba = form.stan_zeba.data
        uzebienie.data_pocz = form.data_pocz.data
        uzebienie.data_kon = form.data_kon.data
        flash('Poprawna edycja stanu uzębienia!', 'success')
        return redirect(url_for('manageTeethCondition', osoba_id=osoba_id))

    form.zab.data = uzebienie.zab
    form.stan_zeba.data = uzebienie.stan_zeba
    form.data_pocz.data = uzebienie.data_pocz
    form.data_kon.data = uzebienie.data_kon
    return render_template('modifyTeethCondition.html', title='Edycja informacji o stanie uzębienia', form=form, osoba=osoba, uzebienie=uzebienie)

@app.route("/addTreatment<int:osoba_id>", methods=['GET', 'POST'])
def addTreatment(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    form = TreatmentForm()
    if osoba.pacjent:
        form = TreatmentForm()
        if form.validate_on_submit():
            flash(f'Poprawnie dodano informacje o zabiegu!', 'success')
            add_nowyzabieg(form.data_zabiegu.data,form.zab.data,form.opis_zabiegu.data,form.kod_uslugi_ICD10.data,form.kod_procedury_ICD9.data,form.ilosc.data,form.mat_kolor.data,osoba.pacjent.lekarzlekarz_id,osoba.pacjent.pacjent_id)
            return redirect(url_for('manageTreatmentHistory', osoba_id=osoba_id))
    else:
        flash(f'Aby dodać informacje o pierwszym zabiegu, najpierw dodaj informacje o stanie zdrowia pacjenta!', 'warning')          
    return render_template('addTreatment.html', title='Dodawanie informacji o zabiegu', form=form, osoba=osoba)

@app.route("/manageTreatmentHistory<int:osoba_id>", methods=['GET', 'POST'])
def manageTreatmentHistory(osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    if osoba.pacjent:
        zabiegi = osoba.pacjent.zabiegi
    else:
        flash(f'Dodaj informacje o pierwszym zabiegu u pacjenta {osoba.imie1} {osoba.nazwisko}!', 'warning')
        zabiegi = [] 
    return render_template('manageTreatmentHistory.html', title='Zarządzanie informacjami o zabiegu', osoba=osoba, zabiegi=zabiegi)

@app.route("/modifyTreatment/<int:zabieg_id>/<int:osoba_id>", methods=['GET', 'POST'])
def modifyTreatment(zabieg_id,osoba_id):
    osoba = db.Osoba.get(osoba_id=osoba_id)
    zabiegi = Zabieg[zabieg_id]
    form = ModifyTreatmentForm()
    if form.validate_on_submit():
        zabiegi.data_zabiegu = form.data_zabiegu.data
        zabiegi.zab = form.zab.data
        zabiegi.opis_zabiegu = form.opis_zabiegu.data
        zabiegi.kod_uslugi_ICD10 = form.kod_uslugi_ICD10.data
        zabiegi.kod_procedury_ICD9 = form.kod_procedury_ICD9.data
        zabiegi.ilosc = form.ilosc.data
        zabiegi.mat_kolor = form.mat_kolor.data
        flash(f'Poprawna edycja informacji o zabiegu {zabiegi.zabieg_id}!', 'success')
        return redirect(url_for('manageTreatmentHistory', osoba_id=osoba_id))

    form.data_zabiegu.data = zabiegi.data_zabiegu
    form.zab.data = zabiegi.zab
    form.opis_zabiegu.data = zabiegi.opis_zabiegu
    form.kod_uslugi_ICD10.data = zabiegi.kod_uslugi_ICD10
    form.kod_procedury_ICD9.data = zabiegi.kod_procedury_ICD9
    form.ilosc.data = zabiegi.ilosc
    form.mat_kolor.data = zabiegi.mat_kolor
    return render_template('modifyTreatment.html', title='Edycja informacji o zabiegu', form=form, osoba=osoba, zabiegi=zabiegi)

@app.route("/managePatientPersonalData<int:osoba_id>", methods=['GET', 'POST'])
def managePatientPersonalData(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    adres = pacjent.adresadres_id
    telefon = pacjent.telefontelefon_id
    return render_template('managePatientPersonalData.html', title='Zarządzanie danymi osobowymi pacjenta', pacjent=pacjent, adres=adres, telefon=telefon)

@app.route("/modifyPersonalData<int:osoba_id>", methods=['GET', 'POST'])
def modifyPersonalData(osoba_id):
    lekarz = Osoba[osoba_id]
    form = ModifyRegistrationForm()
    if form.validate_on_submit():
        lekarz.imie1 = form.name.data
        lekarz.imie2 = form.second_name.data
        lekarz.nazwisko = form.last_name.data
        lekarz.pesel = form.pesel.data
        lekarz.data_ur = form.data_ur.data
        lekarz.plec = form.plec.data
        lekarz.email = form.email.data
        flash('Poprawna edycja danych osobowych!', 'success')
        return redirect(url_for('accountDoctor'))

    form.id.data = lekarz.osoba_id
    form.name.data = lekarz.imie1
    form.second_name.data = lekarz.imie2
    form.last_name.data = lekarz.nazwisko
    form.pesel.data = lekarz.pesel
    form.data_ur.data = lekarz.data_ur
    form.plec.data = lekarz.plec
    form.email.data = lekarz.email            
    return render_template('modifyPersonalData.html', form=form, title='Edycja danych osobowych', buttontext='Edycja danych osobowych')

@app.route("/modifyPatientPersonalData/<int:osoba_id>", methods=['GET', 'POST'])
def modifyPatientPersonalData(osoba_id):
    pacjent = db.Osoba.get(osoba_id=osoba_id)
    form = ModifyRegistrationForm()
    if form.validate_on_submit():
        pacjent.imie1 = form.name.data
        pacjent.imie2 = form.second_name.data
        pacjent.nazwisko = form.last_name.data
        pacjent.pesel = form.pesel.data
        pacjent.data_ur = form.data_ur.data
        pacjent.plec = form.plec.data
        pacjent.email = form.email.data
        flash('Poprawna edycja danych osobowych pacjenta!', 'success')
        return redirect(url_for('managePatientPersonalData', osoba_id=osoba_id))

    form.name.data = pacjent.imie1
    form.second_name.data = pacjent.imie2
    form.last_name.data = pacjent.nazwisko
    form.pesel.data = pacjent.pesel
    form.data_ur.data = pacjent.data_ur
    form.plec.data = pacjent.plec
    form.email.data = pacjent.email            
    return render_template('modifyPatientPersonalData.html', title='Edycja danych osobowych', buttontext='Edycja danych osobowych', form=form, pacjent=pacjent)

@app.route("/findPatient", methods=['GET', 'POST'])
def findPatient():
    form = FindPatientForm()
    if form.validate_on_submit():
        pacjenci = select(pacjent for pacjent in Osoba if (not form.name.data or form.name.data==pacjent.imie1)
        and (not form.last_name.data or form.last_name.data==pacjent.nazwisko)
        and (not form.pesel.data or form.pesel.data==pacjent.pesel)
        and (not form.card_number.data or (pacjent.pacjent and form.card_number.data==pacjent.pacjent.nr_karty))  
            and pacjent.logowanie.rodzaj_konta==1)[:]
        if len(pacjenci)>1:
            flash(f'Poprawnie znaleziono {len(pacjenci)} pacjentów!', 'success')
        elif len(pacjenci)==1:
            flash(f'Poprawnie znaleziono {len(pacjenci)} pacjenta!', 'success')
        else:
            flash(f'Nie udało się znaleźć pacjentów poprzez podane informacje, sprawdź poprawność danych!', 'warning')
        return render_template('showFoundPatients.html', title='Wybieranie pacjenta', pacjenci=pacjenci)             
    return render_template('findPatient.html', title='Wyszukiwanie pacjenta', form=form)

@app.route("/showFoundPatients")
def showFoundPatients():
    return render_template('showFoundPatients.html', title='Wybieranie pacjenta')

