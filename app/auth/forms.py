from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app import models


class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Length(1, 64)], render_kw={"placeholder": "Wpisz swój login"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "Wpisz swoje hasło"})
    submit = SubmitField('Zaloguj')

class RegistrationForm(FlaskForm):
    "Klasa do zmiany - cos sie zepsuło i nei wyswietla komunikatorow, validacje nie dzialaja chyba "
    email = StringField('', validators=[DataRequired(), Length(1, 64),
                                        Email(
                                            message='Email powinnien się składać z małych liter, @ oraz koncówki np. pl')],
                        render_kw={"placeholder": "Wpisz swój email"})
    nrrej = StringField('', validators=[DataRequired(), Length(7, 10,
                                                               message='Numer rejestracyjny powinnien się składać od 7 do 10 liter')],
                        render_kw={"placeholder": "Wpisz swój numer rejestracyjny"})
    numberphone = StringField('', validators=[DataRequired(),
                                              Length(9, 9, message='Numer telefonu powinnien się składać z 9 cyfr')],
                              render_kw={"placeholder": "Wpisz swój numer telefonu"})
    firstname = StringField('', validators=[DataRequired(), Length(3, 20)],
                            render_kw={"placeholder": "Wpisz swoje imie"})
    subname = StringField('', validators=[DataRequired(), Length(3, 20)],
                          render_kw={"placeholder": "Wpisz swoje nazwisko"})
    password = PasswordField('',
                             validators=[DataRequired(), EqualTo('password2', message='Hasła muszą być identyczne.')],
                             render_kw={"placeholder": "Wpisz swoje hasło"})
    password2 = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": "Powtórz hasło"})
    checkbox = BooleanField(
        '<span>Wyrażam zgodę na przetwarzanie danych osobowych zgodnie z postanowieniami <a '
        'href="/regulamin">regulaminu</a></span>',
        validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')


def validate_email(field):
    if models.User.query.filter_by(email=field).first():
        return True
