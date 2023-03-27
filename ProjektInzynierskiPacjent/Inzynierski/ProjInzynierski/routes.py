import os
from flask import render_template, url_for, flash, redirect
from ProjInzynierski import app
from ProjInzynierski.forms import *
from pony.orm import *
from ProjInzynierski.models import *
from flask_bcrypt import Bcrypt
from flask_login import current_user, logout_user, login_user, login_required

bcrypt=Bcrypt()
db.bind(provider='mysql', host='localhost', user='root', passwd='', db='GabinetStomatologiczny')
set_sql_debug(True)
db.generate_mapping(create_tables=True)

@db_session
def add_rejestracjaosoba(imie1,imie2,nazwisko,pesel,data_ur,plec,email):
    Osoba(imie1=imie1,imie2=imie2,nazwisko=nazwisko,pesel=pesel,data_ur=data_ur,plec=plec,email=email)

@db_session
def add_logindoosoby(login,haslo,id_osoby):
    Logowanie(rodzaj_konta=1,login=login,haslo=haslo,osobaosoba_id=id_osoby)

@db_session
def add_nowyadres(wojewodztwo,gmina,miejscowosc,ulica,nr_domu,nr_lokalu,kod_poczt):
    return Adres(wojewodztwo=wojewodztwo,gmina=gmina,miejscowosc=miejscowosc,ulica=ulica,nr_domu=nr_domu,nr_lokalu=nr_lokalu,kod_poczt=kod_poczt)      

@db_session
def add_nowytelefon(telefon_kom1,telefon_kom2,telefon_kom3,telefon_stacj,telefon_stacj2,telefon_zagr,telefon_zagr2):
    return Telefon(czy_telefon=1,telefon_kom1=telefon_kom1,telefon_kom2=telefon_kom2,telefon_kom3=telefon_kom3,telefon_stacj=telefon_stacj,telefon_stacj2=telefon_stacj2,telefon_zagr=telefon_zagr,telefon_zagr2=telefon_zagr2)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():   #jesli wszystko zostalo wpisane odpowiednio
        flash(f'Utworzono konto dla użytkownika {form.name.data} {form.last_name.data}!', 'success')
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        add_rejestracjaosoba(form.name.data,form.second_name.data,form.last_name.data,form.pesel.data,form.data_ur.data,form.plec.data,form.email.data)
        dodanaosoba=db.Osoba.get(pesel=form.pesel.data) #pobierz osobe z bazy danych po numerze pesel
        add_logindoosoby(form.username.data,hashed_password,dodanaosoba)
        dodanaosoba.gabinetgabinet_id=1
        return redirect(url_for('login'))
    return render_template('register.html', title='Zarejestruj się', form=form)

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
            if current_user.rodzaj_konta==1:
                return redirect(url_for('accountPatient'))            
            else:
                flash('Nieznany typ konta', 'danger')
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
            return redirect(url_for('accountPatient'))                
    return render_template('modifyLoginData.html', form=form, title='Edycja danych logowania', buttontext='Edycja danych logowania')

@app.route("/accountPatient", methods=['GET', 'POST'])
def accountPatient():
    pacjent=db.Osoba.get(osoba_id=current_user.osoba_id)
    return render_template('accountPatient.html', title='Konto pacjenta', pacjent=pacjent)

@app.route("/showDoctor<int:osoba_id>", methods=['GET', 'POST'])
def showDoctor(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    czy_pacjent = osoba.pacjent
    doktor = []
    dane_lekarza = []
    if not czy_pacjent:
        flash(f'Aby wyświetlić informacje o lekarzu prowadzącym, poproś lekarza o przypisanie siebie do twojego konta!', 'warning')
        doktor = []
    else:
        doktor = czy_pacjent.lekarzlekarz_id
        dane_lekarza = doktor.osobaosoba_id
    return render_template('showDoctor.html', title='Informacje o lekarzu', osoba=osoba, doktor=doktor, dane_lekarza=dane_lekarza)

@app.route("/showHealthCondition<int:osoba_id>", methods=['GET', 'POST'])
def showHealthCondition(osoba_id):
    stanzdrowia = db.Pacjent.get(osobaosoba_id=current_user.osoba_id)
    if not stanzdrowia:
        flash(f'Poproś lekarza o dodanie poniższych informacji!', 'warning')
        stanzdrowia = [] 
    return render_template('showHealthCondition.html', title='Stan zdrowia i jamy ustnej', stanzdrowia=stanzdrowia)

@app.route("/addHomeAddress", methods=['GET', 'POST'])
def addHomeAddress():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    form = AddressForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano adres zamieszkania!', 'success')
        dodanyadres = add_nowyadres(form.wojewodztwo.data,form.gmina.data,form.miejscowosc.data,form.ulica.data,form.nr_domu.data,form.nr_lokalu.data,form.kod_poczt.data)
        dodanyadres.flush()
        osoba.adresadres_id = dodanyadres.adres_id
        return redirect(url_for('manageHomeAddress', osoba_id=current_user.osoba_id))
    return render_template('addHomeAddress.html', title='Dodawanie adresu zamieszkania', form=form, osoba=osoba)

@app.route("/manageHomeAddress<int:osoba_id>")
def manageHomeAddress(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    adres = osoba.adresadres_id
    return render_template('manageHomeAddress.html', title='Zarządzanie adresem zamieszkania', osoba=osoba, adres=adres)

@app.route("/modifyHomeAddress", methods=['GET', 'POST'])
def modifyHomeAddress():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    adres = osoba.adresadres_id
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
        return redirect(url_for('manageHomeAddress', osoba_id=current_user.osoba_id))

    form.wojewodztwo.data = adres.wojewodztwo
    form.gmina.data = adres.gmina
    form.miejscowosc.data = adres.miejscowosc
    form.ulica.data = adres.ulica
    form.nr_domu.data = adres.nr_domu
    form.nr_lokalu.data = adres.nr_lokalu
    form.kod_poczt.data = adres.kod_poczt
    return render_template('modifyHomeAddress.html', form=form, title='Edycja adresu zamieszkania', osoba=osoba, adres=adres)

@app.route("/addHomeTelephone", methods=['GET', 'POST'])
def addHomeTelephone():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    form = TelephoneForm()
    if form.validate_on_submit():
        flash(f'Poprawnie dodano telefon kontaktowy!', 'success')
        dodanytelefon = add_nowytelefon(form.telefon_kom1.data,form.telefon_kom2.data,form.telefon_kom3.data,form.telefon_stacj.data,form.telefon_stacj2.data,form.telefon_zagr.data,form.telefon_zagr2.data)
        dodanytelefon.flush()
        osoba.telefontelefon_id = dodanytelefon.telefon_id
        return redirect(url_for('manageHomeTelephone', osoba_id=current_user.osoba_id)) 
    return render_template('addHomeTelephone.html', title='Dodawanie telefonu kontaktowego', form=form, osoba=osoba)

@app.route("/manageHomeTelephone<int:osoba_id>")
def manageHomeTelephone(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    telefon = osoba.telefontelefon_id    
    return render_template('manageHomeTelephone.html', title='Zarządzanie telefonem kontaktowym', osoba=osoba, telefon=telefon)

@app.route("/modifyHomeTelephone", methods=['GET', 'POST'])
def modifyHomeTelephone():
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    telefon = osoba.telefontelefon_id
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
        return redirect(url_for('manageHomeTelephone', osoba_id=current_user.osoba_id))

    form.telefon_kom1.data = telefon.telefon_kom1
    form.telefon_kom2.data = telefon.telefon_kom2
    form.telefon_kom3.data = telefon.telefon_kom3
    form.telefon_stacj.data = telefon.telefon_stacj
    form.telefon_stacj2.data = telefon.telefon_stacj2
    form.telefon_zagr.data = telefon.telefon_zagr
    form.telefon_zagr2.data = telefon.telefon_zagr2
    return render_template('modifyHomeTelephone.html', title='Edycja telefonu kontaktowego', form=form, osoba=osoba, telefon=telefon)

@app.route("/showOffice<int:osoba_id>")
def showOffice(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    gabinet = osoba.gabinetgabinet_id
    adresdogabinetu = gabinet.adresadres_id
    telefondogabinetu = gabinet.telefontelefon_id
    return render_template('showOffice.html', title='Informacje o gabinecie', osoba=osoba, gabinet=gabinet, adresdogabinetu=adresdogabinetu, telefondogabinetu=telefondogabinetu)

@app.route("/showPrescriptions<int:osoba_id>")
def showPrescriptions(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    recepty = []
    if osoba.pacjent:
        if osoba.pacjent.recepty:
            recepty = osoba.pacjent.recepty
        else: 
            flash(f'Poproś lekarza o dodanie pierwszego wpisu o recepcie!', 'warning')
    else:
        flash(f'Aby zobaczyć wystawione recepty, poproś lekarza o dodanie informacji o stanie zdrowia!', 'warning')
        recepty = []   
    return render_template('showPrescriptions.html', title='Wystawione recepty', osoba=osoba, recepty=recepty)

@app.route("/showTeethCondition<int:osoba_id>")
def showTeethCondition(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    uzebienie = []
    if osoba.pacjent:
        if osoba.pacjent.uzebienie:
            uzebienie = osoba.pacjent.uzebienie
        else:
            flash(f'Poproś lekarza o dodanie pierwszego wpisu o stanie uzębienia!', 'warning')
    else:
        flash(f'Aby zobaczyć informacje o stanie uzębienia, poproś lekarza o dodanie informacji o stanie zdrowia i jamy ustnej!', 'warning')
        uzebienie = []    
    return render_template('showTeethCondition.html', title='Stan uzębienia', osoba=osoba, uzebienie=uzebienie)

@app.route("/showTreatmentHistory<int:osoba_id>")
def showTreatmentHistory(osoba_id):
    osoba = db.Osoba.get(osoba_id=current_user.osoba_id)
    zabiegi = []
    if osoba.pacjent:
        if osoba.pacjent.zabiegi:
            zabiegi = osoba.pacjent.zabiegi
        else:
            flash(f'Poproś lekarza o dodanie pierwszego wpisu o zabiegu!', 'warning')
    else:
        flash(f'Aby zobaczyć historię zabiegów, poproś lekarza o dodanie informacji o stanie zdrowia!', 'warning')
        zabiegi = []
    return render_template('showTreatmentHistory.html', title='Historia zabiegów', osoba=osoba, zabiegi=zabiegi)

@app.route("/modifyPersonalData<int:osoba_id>", methods=['GET', 'POST'])
def modifyPersonalData(osoba_id):
    pacjent = Osoba[osoba_id]
    form = ModifyRegistrationForm()
    if form.validate_on_submit():
        pacjent.imie1 = form.name.data
        pacjent.imie2 = form.second_name.data
        pacjent.nazwisko = form.last_name.data
        pacjent.pesel = form.pesel.data
        pacjent.data_ur = form.data_ur.data
        pacjent.plec = form.plec.data
        pacjent.email = form.email.data
        flash('Poprawna edycja danych osobowych!', 'success')
        return redirect(url_for('accountPatient'))

    form.id.data = pacjent.osoba_id
    form.name.data = pacjent.imie1
    form.second_name.data = pacjent.imie2
    form.last_name.data = pacjent.nazwisko
    form.pesel.data = pacjent.pesel
    form.data_ur.data = pacjent.data_ur
    form.plec.data = pacjent.plec
    form.email.data = pacjent.email            
    return render_template('modifyPersonalData.html', form=form, title='Edycja danych osobowych', buttontext='Edycja danych osobowych')

