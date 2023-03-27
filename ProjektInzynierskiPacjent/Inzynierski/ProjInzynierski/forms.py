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
                           validators=[DataRequired(), Length(min=6, max=13, message='Kod pocztowy powinien składać się od 6 do 13 znaków!')])
    submit = SubmitField('Dodaj adres zamieszkania')
    cancel = SubmitField('Anuluj')


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
    cancel = SubmitField('Anuluj')


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
    submit = SubmitField('Dodaj telefon kontaktowy')


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
    submit = SubmitField('Edytuj telefon kontaktowy')

