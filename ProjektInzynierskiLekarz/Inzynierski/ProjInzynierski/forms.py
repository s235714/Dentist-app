from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError, Optional, NumberRange
from ProjInzynierski.models import Osoba, Logowanie, Lekarz, Pacjent
from ProjInzynierski import db
from flask_login import current_user, logout_user, login_user, login_required, AnonymousUserMixin


class RegistrationForm(FlaskForm):
    name = StringField('Imię*',
                           validators=[DataRequired(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    second_name = StringField('Drugie imię',
                           validators=[Optional(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    last_name = StringField('Nazwisko*',
                           validators=[DataRequired(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    pesel = StringField('Numer PESEL*',
                           validators=[DataRequired(), Length(min=11, max=11, message='PESEL powinien zawierać 11 znaków!')])
    data_ur = StringField('Data urodzenia',
                           validators=[Optional(), Length(max=10, message='Data urodzenia powinna być w formie RRRR-MM-DD!')])
    plec = StringField('Płeć*',
                           validators=[DataRequired(), Length(max=1, message='m - mężczyzna, k - kobieta')])
    email = StringField('Adres e-mail',
                           validators=[Optional(), Email(message='Nieprawidłowy adres email!')])
    username = StringField('Login*',
                           validators=[DataRequired(), Length(min=6, max=50, message='Login powinien zawierać od 6 do 50 znaków!')])
    password = PasswordField('Hasło*', validators=[InputRequired(),Length(min=7, max=20, message='Hasło powinno składać się z co najmniej 7 znaków!')])
    confirm_password = PasswordField('Powtórz hasło*',
                                     validators=[DataRequired(), EqualTo('password',message='Hasła nie są identyczne!')])
    submit = SubmitField('Zarejestruj się')

    def validate_email(self, email):
        user = db.Osoba.get(email=email.data)
        if user:
            raise ValidationError('Ten adres email jest już zajęty!')

    def validate_pesel(self, pesel):
        user = db.Osoba.get(pesel=pesel.data)
        if user:
            raise ValidationError('Ten numer PESEL należy do innej osoby!')

    def validate_username(self, username):
        user = db.Logowanie.get(login=username.data)
        if user:
            raise ValidationError('Ten login jest już zajęty!')


class AddNewPatientForm(FlaskForm):
    name = StringField('Imię*',
                           validators=[DataRequired(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    second_name = StringField('Drugie imię',
                           validators=[Optional(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    last_name = StringField('Nazwisko*',
                           validators=[DataRequired(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    pesel = StringField('Numer PESEL*',
                           validators=[DataRequired(), Length(min=11, max=11, message='PESEL powinien zawierać 11 znaków!')])
    data_ur = StringField('Data urodzenia (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data urodzenia powinna być w formie RRRR-MM-DD!')])
    plec = StringField('Płeć*',
                           validators=[DataRequired(), Length(max=1, message='m - mężczyzna, k - kobieta')])
    email = StringField('Adres e-mail',
                           validators=[Optional(), Email(message='Nieprawidłowy adres email!')])
    username = StringField('Login*',
                           validators=[DataRequired(), Length(min=6, max=50, message='Login powinien zawierać od 6 do 50 znaków!')])
    password = PasswordField('Hasło*', validators=[InputRequired(),Length(min=7, max=20, message='Hasło powinno składać się z co najmniej 7 znaków!')])
    confirm_password = PasswordField('Powtórz hasło*',
                                     validators=[DataRequired(), EqualTo('password',message='Hasła nie są identyczne!')])
    submit = SubmitField('Dodaj nowego pacjenta')

    def validate_email(self, email):
        user = db.Osoba.get(email=email.data)
        if user:
            raise ValidationError('Ten adres email jest już zajęty!')

    def validate_pesel(self, pesel):
        user = db.Osoba.get(pesel=pesel.data)
        if user:
            raise ValidationError('Ten numer PESEL należy do innej osoby!')

    def validate_username(self, username):
        user = db.Logowanie.get(login=username.data)
        if user:
            raise ValidationError('Ten login jest już zajęty!')


class ModifyRegistrationForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Imię*',
                           validators=[DataRequired(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    second_name = StringField('Drugie imię',
                           validators=[Optional(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    last_name = StringField('Nazwisko*',
                           validators=[DataRequired(), Length(min=2, max=50, message='Pole powinno zawierać od 2 do 50 znaków!')])
    pesel = StringField('PESEL*',
                           validators=[DataRequired(), Length(min=11, max=11, message='PESEL powinien zawierać 11 znaków!')])
    data_ur = StringField('Data urodzenia (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data urodzenia powinna być w formie RRRR-MM-DD!')])
    plec = StringField('Płeć*',
                           validators=[DataRequired(), Length(max=1, message='m - mężczyzna, k - kobieta')])
    email = StringField('Email',
                           validators=[Optional(), Email(message='Nieprawidłowy adres email!')])
    submit = SubmitField('Edytuj dane osobowe')

    def validate_email(self, email):
        user = db.Osoba.get(email=email.data)
        if user and (str(user.osoba_id)!=self.id.data):
            raise ValidationError('Ten adres email jest już zajęty!')

    def validate_pesel(self, pesel):
        user = db.Osoba.get(pesel=pesel.data)
        if user and (str(user.osoba_id)!=self.id.data):
            raise ValidationError(f'Ten numer PESEL należy do innej osoby!')


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')


class ModifyLoginForm(FlaskForm):
    id = HiddenField('id')
    #username = StringField('Login',
    #                      validators=[DataRequired(), Length(min=3, max=50, message='Login powinien zawierać od 3 do 50 znaków!')])
    password = PasswordField('Stare hasło*', validators=[InputRequired(),Length(min=7, max=20, message='Pole powinno zawierać stare hasło!')])
    new_password = PasswordField('Nowe hasło*', validators=[InputRequired(),Length(min=7, max=20, message='Nowe hasło powinno składać się z co najmniej 7 znaków!')])
    confirm_new_password = PasswordField('Powtórz nowe hasło*', validators=[DataRequired(), EqualTo('new_password',message='Hasła nie są identyczne!')])
    submit = SubmitField('Edytuj hasło dostępu')

    '''def validate_username(self, username):
        user = db.Logowanie.get(login=username.data)
        if user and (str(user.osoba.osoba_id)!=self.id.data):
            raise ValidationError('Ten login jest już zajęty!')'''    

    def validate_old_password(self, password):
        user = db.Logowanie.get(password=password.data)
        if user:
            raise ValidationError('Stare hasło jest nieprawidłowe!')

    '''def validate_new_password(self, new_password):
        user = db.Logowanie.get(password=new_password.data)
        if user:
            raise ValidationError('Nowe hasło nie może być identyczne jak stare!')'''


class DoctorForm(FlaskForm):
    licence_number = StringField('Numer licencji lekarza',
                           validators=[Optional(), Length(max=20, message='Pole powinno zawierać maksymalnie 20 znaków!')])
    date_upr = StringField('Data uzyskania uprawnień (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data uzyskania uprawnień powinna być w formie RRRR-MM-DD!')])
    specjalizacje = StringField('Specjalizacje',
                           validators=[Optional(), Length(max=250, message='Pole powinno zawierać maksymalnie 250 znaków!')])
    submit = SubmitField('Dodaj informacje o lekarzu')

    '''def validate_licence_number(self, numer_licen):
        user = db.Lekarz.get(numer_licen=licence_number.data)
        if user:
            raise ValidationError('Ten numer licencji należy do innego lekarza!')'''


class ModifyDoctorForm(FlaskForm):
    licence_number = StringField('Numer licencji lekarza',
                           validators=[Optional(), Length(max=20, message='Pole powinno zawierać maksymalnie 20 znaków!')])
    date_upr = StringField('Data uzyskania uprawnień (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data uzyskania uprawnień powinna być w formie RRRR-MM-DD!')])
    specjalizacje = StringField('Specjalizacje',
                           validators=[Optional(), Length(max=250, message='Pole powinno zawierać maksymalnie 250 znaków!')])
    submit = SubmitField('Edytuj informacje o lekarzu')

    '''def validate_licence_number(self, numer_licen):
        user = db.Lekarz.get(numer_licen=licence_number.data)
        if user:
            raise ValidationError('Ten numer licencji należy do innego lekarza!')'''


class PatientForm(FlaskForm):
    card_number = StringField('Numer karty pacjenta*',
                           validators=[DataRequired(), Length(max=10, message='Pole powinno zawierać maksymalnie 10 znaków!')])
    higiena = StringField('Higiena',
                           validators=[Optional(), Length(max=60, message='Pole powinno zawierać maksymalnie 60 znaków!')])
    zgryz = StringField('Zgryz',
                           validators=[Optional(), Length(max=80, message='Pole powinno zawierać maksymalnie 80 znaków!')])
    blona_sluzowa = StringField('Błona śluzowa',
                           validators=[Optional(), Length(max=60, message='Pole powinno zawierać maksymalnie 60 znaków!')])
    uzup_protet = TextAreaField('Uzupełnienia protetyczne', render_kw={"rows": 10, "cols": 5})
    przyzebie = TextAreaField('Przyzębie', render_kw={"rows": 10, "cols": 5})
    choroby = TextAreaField('Choroby ogólnoustrojowe', render_kw={"rows": 10, "cols": 5})
    leki = TextAreaField('Zażywane leki', render_kw={"rows": 10, "cols": 5})
    uczulenia = TextAreaField('Uczulenia', render_kw={"rows": 10, "cols": 5})
    czy_dziecko = StringField('Czy osoba jest dzieckiem (poniżej 18. roku życia)?',
                           validators=[Optional(), Length(min=3, max=3, message='Pole powinno zawierać słowo tak lub nie!')])                                                          
    submit = SubmitField('Dodaj informacje o stanie zdrowia')

    '''def validate_card_number(self, nr_karty):
        user = db.Pacjent.get(nr_karty=card_number.data)
        if user:
            raise ValidationError('Ten numer karty należy do innego pacjenta!')'''


class ModifyPatientForm(FlaskForm):
    card_number = StringField('Numer karty pacjenta*',
                           validators=[DataRequired(), Length(max=10, message='Pole powinno zawierać maksymalnie 10 znaków!')])
    higiena = StringField('Higiena',
                           validators=[Optional(), Length(max=60, message='Pole powinno zawierać maksymalnie 60 znaków!')])
    zgryz = StringField('Zgryz',
                           validators=[Optional(), Length(max=80, message='Pole powinno zawierać maksymalnie 80 znaków!')])
    blona_sluzowa = StringField('Błona śluzowa',
                           validators=[Optional(), Length(max=60, message='Pole powinno zawierać maksymalnie 60 znaków!')])
    uzup_protet = TextAreaField('Uzupełnienia protetyczne', render_kw={"rows": 10, "cols": 5})
    przyzebie = TextAreaField('Przyzębie', render_kw={"rows": 10, "cols": 5})
    choroby = TextAreaField('Choroby ogólnoustrojowe', render_kw={"rows": 10, "cols": 5})
    leki = TextAreaField('Zażywane leki', render_kw={"rows": 10, "cols": 5})
    uczulenia = TextAreaField('Uczulenia', render_kw={"rows": 10, "cols": 5})
    czy_dziecko = StringField('Czy osoba jest dzieckiem (poniżej 18. roku życia)?',
                           validators=[Optional(), Length(min=3, max=3, message='Pole powinno zawierać słowo tak lub nie!')])                                                          
    submit = SubmitField('Edytuj informacje o stanie zdrowia')

    '''def validate_card_number(self, nr_karty):
        user = db.Pacjent.get(nr_karty=card_number.data)
        if user:
            raise ValidationError('Ten numer karty należy do innego pacjenta!')'''


class AddressForm(FlaskForm):
    wojewodztwo = StringField('Województwo',
                           validators=[Optional(), Length(max=50, message='Nazwa województwa powinna składać się z maksymalnie 50 znaków!')])
    gmina = StringField('Gmina',
                           validators=[Optional(), Length(max=50, message='Nazwa gminy powinna składać się z maksymalnie 50 znaków!')])
    miejscowosc = StringField('Miejscowość*',
                           validators=[DataRequired(), Length(max=60, message='Nazwa miejscowości powinna składać się z maksymalnie 60 znaków!')])
    ulica = StringField('Ulica',
                           validators=[Optional(), Length(max=70, message='Nazwa ulicy powinna składać się z maksymalnie 70 znaków!')])
    nr_domu = StringField('Numer domu*',
                           validators=[DataRequired(), Length(max=10, message='Numer domu powinien składać się z maksymalnie 10 znaków!')])
    nr_lokalu = StringField('Numer lokalu',
                           validators=[Optional(), Length(max=10, message='Numer lokalu powinien składać się z maksymalnie 10 znaków!')])
    kod_poczt = StringField('Kod pocztowy*',
                           validators=[DataRequired(), Length(min=6,max=13, message='Kod pocztowy powinien składać się od 6 do 13 znaków!')])
    submit = SubmitField('Dodaj adres zamieszkania')


class OfficeAddressForm(FlaskForm):
    miejscowosc = StringField('Miejscowość*',
                           validators=[DataRequired(), Length(max=60, message='Nazwa miejscowości powinna składać się z maksymalnie 60 znaków!')])
    ulica = StringField('Ulica',
                           validators=[Optional(), Length(max=70, message='Nazwa ulicy powinna składać się z maksymalnie 70 znaków!')])
    nr_domu = StringField('Numer domu*',
                           validators=[DataRequired(), Length(max=10, message='Numer domu powinien składać się z maksymalnie 10 znaków!')])
    nr_lokalu = StringField('Numer lokalu',
                           validators=[Optional(), Length(max=10, message='Numer lokalu powinien składać się z maksymalnie 10 znaków!')])
    kod_poczt = StringField('Kod pocztowy*',
                           validators=[DataRequired(), Length(min=6,max=13, message='Kod pocztowy powinien składać się od 6 do 13 znaków!')])
    submit = SubmitField('Dodaj adres gabinetu')


class ModifyAddressForm(FlaskForm):
    wojewodztwo = StringField('Województwo',
                           validators=[Optional(), Length(max=50, message='Nazwa województwa powinna składać się z maksymalnie 50 znaków!')])
    gmina = StringField('Gmina',
                           validators=[Optional(), Length(max=50, message='Nazwa gminy powinna składać się z maksymalnie 50 znaków!')])
    miejscowosc = StringField('Miejscowość*',
                           validators=[DataRequired(), Length(max=60, message='Nazwa miejscowości powinna składać się z maksymalnie 60 znaków!')])
    ulica = StringField('Ulica',
                           validators=[Optional(), Length(max=70, message='Nazwa ulicy powinna składać się z maksymalnie 70 znaków!')])
    nr_domu = StringField('Numer domu*',
                           validators=[DataRequired(), Length(max=10, message='Numer domu powinien składać się z maksymalnie 10 znaków!')])
    nr_lokalu = StringField('Numer lokalu',
                           validators=[Optional(), Length(max=10, message='Numer lokalu powinien składać się z maksymalnie 10 znaków!')])
    kod_poczt = StringField('Kod pocztowy*',
                           validators=[DataRequired(), Length(min=6,max=13, message='Kod pocztowy powinien składać się od 6 do 13 znaków!')])
    submit = SubmitField('Edytuj adres zamieszkania')


class ModifyOfficeAddressForm(FlaskForm):
    miejscowosc = StringField('Miejscowość*',
                           validators=[DataRequired(), Length(max=60, message='Nazwa miejscowości powinna składać się z maksymalnie 60 znaków!')])
    ulica = StringField('Ulica',
                           validators=[Optional(), Length(max=70, message='Nazwa ulicy powinna składać się z maksymalnie 70 znaków!')])
    nr_domu = StringField('Numer domu*',
                           validators=[DataRequired(), Length(max=10, message='Numer domu powinien składać się z maksymalnie 10 znaków!')])
    nr_lokalu = StringField('Numer lokalu',
                           validators=[Optional(), Length(max=10, message='Numer lokalu powinien składać się z maksymalnie 10 znaków!')])
    kod_poczt = StringField('Kod pocztowy*',
                           validators=[DataRequired(), Length(min=6,max=13, message='Kod pocztowy powinien składać się od 6 do 13 znaków!')])
    submit = SubmitField('Edytuj adres gabinetu')


class TelephoneForm(FlaskForm):
    telefon_kom1 = StringField('Numer telefonu komórkowego 1',
                           validators=[Optional(), Length(max=10, message='Numer telefonu komórkowego powinien składać się z maksymalnie 10 znaków!')])
    telefon_kom2 = StringField('Numer telefonu komórkowego 2',
                           validators=[Optional(), Length(max=10, message='Numer telefonu komórkowego powinien składać się z maksymalnie 10 znaków!')])
    telefon_kom3 = StringField('Numer telefonu komórkowego 3',
                           validators=[Optional(), Length(max=10, message='Numer telefonu komórkowego powinien składać się z maksymalnie 10 znaków!')])
    telefon_stacj = StringField('Numer telefonu stacjonarnego 1',
                           validators=[Optional(), Length(max=10, message='Numer telefonu stacjonarnego powinien składać się z maksymalnie 10 znaków!')])
    telefon_stacj2 = StringField('Numer telefonu stacjonarnego 2',
                           validators=[Optional(), Length(max=10, message='Numer telefonu stacjonarnego powinien składać się z maksymalnie 10 znaków!')])
    telefon_zagr = StringField('Numer telefonu zagranicznego 1',
                           validators=[Optional(), Length(max=19, message='Numer telefonu zagranicznego powinien składać się z maksymalnie 19 znaków!')])    
    telefon_zagr2 = StringField('Numer telefonu zagranicznego 2',
                           validators=[Optional(), Length(max=19, message='Numer telefonu zagranicznego powinien składać się z maksymalnie 19 znaków!')]) 
    submit = SubmitField('Dodaj telefon')


class ModifyTelephoneForm(FlaskForm):
    telefon_kom1 = StringField('Numer telefonu komórkowego 1',
                           validators=[Optional(), Length(max=10, message='Numer telefonu komórkowego powinien składać się z maksymalnie 10 znaków!')])
    telefon_kom2 = StringField('Numer telefonu komórkowego 2',
                           validators=[Optional(), Length(max=10, message='Numer telefonu komórkowego powinien składać się z maksymalnie 10 znaków!')])
    telefon_kom3 = StringField('Numer telefonu komórkowego 3',
                           validators=[Optional(), Length(max=10, message='Numer telefonu komórkowego powinien składać się z maksymalnie 10 znaków!')])
    telefon_stacj = StringField('Numer telefonu stacjonarnego 1',
                           validators=[Optional(), Length(max=10, message='Numer telefonu stacjonarnego powinien składać się z maksymalnie 10 znaków!')])
    telefon_stacj2 = StringField('Numer telefonu stacjonarnego 2',
                           validators=[Optional(), Length(max=10, message='Numer telefonu stacjonarnego powinien składać się z maksymalnie 10 znaków!')])
    telefon_zagr = StringField('Numer telefonu zagranicznego 1',
                           validators=[Optional(), Length(max=19, message='Numer telefonu zagranicznego powinien składać się z maksymalnie 19 znaków!')])    
    telefon_zagr2 = StringField('Numer telefonu zagranicznego 2',
                           validators=[Optional(), Length(max=19, message='Numer telefonu zagranicznego powinien składać się z maksymalnie 19 znaków!')]) 
    submit = SubmitField('Edytuj telefon')


class OfficeForm(FlaskForm):
    nazwa = StringField('Nazwa gabinetu stomatologicznego*',
                           validators=[DataRequired(), Length(max=300, message='Nazwa gabinetu stomatologicznego powinna składać się z maksymalnie 300 znaków!')])
    regon = StringField('Numer REGON',
                           validators=[Optional(), Length(min=9, max=14, message='Numer REGON powinien zawierać od 9 do 14 znaków!')])
    nip = StringField('Numer NIP',
                           validators=[Optional(), Length(min=13, max=13, message='Numer NIP powinien składać się z 10. cyfr i być zapisany w formie 000-000-00-00!')])    
    submit = SubmitField('Dodaj informacje o gabinecie')


class ModifyOfficeForm(FlaskForm):
    nazwa = StringField('Nazwa gabinetu stomatologicznego*',
                           validators=[DataRequired(), Length(max=300, message='Nazwa gabinetu stomatologicznego powinna składać się z maksymalnie 300 znaków!')])
    regon = StringField('Numer REGON',
                           validators=[Optional(), Length(min=9, max=14, message='Numer REGON powinien zawierać od 9 do 14 znaków!')])
    nip = StringField('Numer NIP',
                           validators=[Optional(), Length(min=13, max=13, message='Numer NIP powinien składać się z 10. cyfr i być zapisany w formie 000-000-00-00!')])    
    submit = SubmitField('Edytuj informacje o gabinecie')


class PrescriptionForm(FlaskForm):
    prescription_num = StringField('Numer recepty',
                           validators=[Optional(), Length(min=22,max=22, message='Numer recepty powinien składać się z 22 cyfr!')])
    oddz_NFZ = StringField('Kod ddziału NFZ*',
                           validators=[DataRequired(), Length(min=1, max=2, message='Kod ddziału NFZ powinien składać się z 2 cyfr od 01 do 16!')])
    upraw_dod = StringField('Uprawnienia dodatkowe pacjenta',
                           validators=[Optional(), Length(max=10, message='Pole powinno zawierać maksymalnie 10 znaków!')])
    odplatnosc = StringField('Odpłatność za leki',
                           validators=[Optional(), Length(max=10, message='Odpłatność za leki powinna składać się z maksymalnie 10 znaków!')])
    przep_leki = TextAreaField('Wypisane leki na recepcie*', render_kw={"rows": 10, "cols": 5})
    data_wyst = StringField('Data wystawienia recepty (musi być w formie RRRR-MM-DD)*',
                           validators=[DataRequired(), Length(max=10, message='Data wystawienia recepty powinna być w formie RRRR-MM-DD!')])
    data_realiz = StringField('Data realizacji od dnia (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data realizacji od dnia powinna być w formie RRRR-MM-DD!')])
    submit = SubmitField('Dodaj informacje o recepcie')

    '''def validate_prescription_num(self, nr_recepty):
        user = db.Recepta.get(nr_recepty=prescription_num.data)
        if user:
            raise ValidationError('Ten numer recepty należy do innej recepty!')'''


class ModifyPrescriptionForm(FlaskForm):
    prescription_num = StringField('Numer recepty',
                           validators=[Optional(), Length(min=22,max=22, message='Numer recepty powinien składać się z 22 cyfr!')])
    oddz_NFZ = StringField('Kod ddziału NFZ*',
                           validators=[DataRequired(), Length(min=1, max=2, message='Kod ddziału NFZ powinien składać się z 2 cyfr od 01 do 16!')])
    upraw_dod = StringField('Uprawnienia dodatkowe pacjenta',
                           validators=[Optional(), Length(max=10, message='Pole powinno zawierać maksymalnie 10 znaków!')])
    odplatnosc = StringField('Odpłatność za leki',
                           validators=[Optional(), Length(max=10, message='Odpłatność za leki powinna składać się z maksymalnie 10 znaków!')])
    przep_leki = TextAreaField('Wypisane leki na recepcie*', render_kw={"rows": 10, "cols": 5})
    data_wyst = StringField('Data wystawienia recepty (musi być w formie RRRR-MM-DD)*',
                           validators=[DataRequired(), Length(max=10, message='Data wystawienia recepty powinna być w formie RRRR-MM-DD!')])
    data_realiz = StringField('Data realizacji od dnia (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data realizacji od dnia powinna być w formie RRRR-MM-DD!')])
    submit = SubmitField('Edytuj informacje o recepcie')

    '''def validate_prescription_num(self, nr_recepty):
        user = db.Recepta.get(nr_recepty=prescription_num.data)
        if user:
            raise ValidationError('Ten numer recepty należy do innej recepty!')'''


class TreatmentForm(FlaskForm):
    data_zabiegu = StringField('Data przeprowadzenia zabiegu (musi być w formie RRRR-MM-DD)*',
                           validators=[DataRequired(), Length(max=10, message='Data przeprowadzenia zabiegu powinna być w formie RRRR-MM-DD!')])
    zab = StringField('Wyleczony ząb',
                           validators=[Optional(), Length(max=20, message='Pole powinno zawierać maksymalnie 20 znaków!')])
    opis_zabiegu = TextAreaField('Opis zabiegu i zalecenia dla pacjenta*', render_kw={"rows": 10, "cols": 5})
    kod_uslugi_ICD10 = StringField('Kod usługi ICD10',
                           validators=[Optional(), Length(max=5, message='Kod usługi ICD10 powinien składać się z maksymalnie 5 znaków!')])
    kod_procedury_ICD9 = StringField('Kod procedury ICD9',
                           validators=[Optional(), Length(max=3, message='Kod procedury ICD9 powinien składać się z maksymalnie 3 znaków!')])
    ilosc = StringField('Ilość wyleczonych zębów',
                           validators=[Optional(), Length(max=10, message='Pole powinno zawierać maksymalnie 10 znaków!')])
    mat_kolor = StringField('Rodzaj i kolor użytych materiałów',
                           validators=[Optional(), Length(max=200, message='Pole powinno zawierać maksymalnie 200 znaków!')])
    submit = SubmitField('Dodaj informacje o zabiegu')


class ModifyTreatmentForm(FlaskForm):
    data_zabiegu = StringField('Data przeprowadzenia zabiegu (musi być w formie RRRR-MM-DD)*',
                           validators=[DataRequired(), Length(max=10, message='Data przeprowadzenia zabiegu powinna być w formie RRRR-MM-DD!')])
    zab = StringField('Wyleczony ząb',
                           validators=[Optional(), Length(max=20, message='Pole powinno zawierać maksymalnie 20 znaków!')])
    opis_zabiegu = TextAreaField('Opis zabiegu i zalecenia dla pacjenta*', render_kw={"rows": 10, "cols": 5})
    kod_uslugi_ICD10 = StringField('Kod usługi ICD10',
                           validators=[Optional(), Length(max=5, message='Kod usługi ICD10 powinien składać się z maksymalnie 5 znaków!')])
    kod_procedury_ICD9 = StringField('Kod procedury ICD9',
                           validators=[Optional(), Length(max=3, message='Kod procedury ICD9 powinien składać się z maksymalnie 3 znaków!')])
    ilosc = StringField('Ilość wyleczonych zębów',
                           validators=[Optional(), Length(max=10, message='Pole powinno zawierać maksymalnie 10 znaków!')])
    mat_kolor = StringField('Rodzaj i kolor użytych materiałów',
                           validators=[Optional(), Length(max=200, message='Pole powinno zawierać maksymalnie 200 znaków!')])
    submit = SubmitField('Edytuj informacje o zabiegu')


class TeethForm(FlaskForm):
    zab = StringField('Ząb',
                           validators=[Optional(), Length(max=20, message='Pole powinno zawierać maksymalnie 20 znaków!')])
    stan_zeba = StringField('Opis stanu zęba',
                           validators=[Optional(), Length(max=200, message='Pole powinno zawierać maksymalnie 200 znaków!')])
    data_pocz = StringField('Data początkowa wystąpienia opisanego stanu zęba (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data początkowa wystąpienia opisanego stanu zęba powinna być w formie RRRR-MM-DD!')])
    data_kon = StringField('Data końcowa wystąpienia opisanego stanu zęba (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data końcowa wystąpienia opisanego stanu zęba powinna być w formie RRRR-MM-DD!')])
    submit = SubmitField('Dodaj informacje o stanie zęba')


class ModifyTeethForm(FlaskForm):
    zab = StringField('Ząb',
                           validators=[Optional(), Length(max=20, message='Pole powinno zawierać maksymalnie 20 znaków!')])
    stan_zeba = StringField('Opis stanu zęba',
                           validators=[Optional(), Length(max=200, message='Pole powinno zawierać maksymalnie 200 znaków!')])
    data_pocz = StringField('Data początkowa wystąpienia opisanego stanu zęba (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data początkowa wystąpienia opisanego stanu zęba powinna być w formie RRRR-MM-DD!')])
    data_kon = StringField('Data końcowa wystąpienia opisanego stanu zęba (musi być w formie RRRR-MM-DD)',
                           validators=[Optional(), Length(max=10, message='Data końcowa wystąpienia opisanego stanu zęba powinna być w formie RRRR-MM-DD!')])
    submit = SubmitField('Edytuj informacje o stanie zęba')


class FindPatientForm(FlaskForm):
    name = StringField('Imię',
                           validators=[Optional(), Length(min=2, max=50, message='Pole powinno zawierać całe imię pacjenta!')])
    last_name = StringField('Nazwisko',
                           validators=[Optional(), Length(min=2, max=50, message='Pole powinno zawierać całe nazwisko pacjenta!')])
    pesel = StringField('Numer PESEL',
                           validators=[Optional(), Length(min=11, max=11, message='Pole powinno zawierać cały numer PESEL pacjenta!')])
    card_number = IntegerField('Numer karty pacjenta',
                           validators=[Optional()])
    submit = SubmitField('Wyszukaj pacjenta')

