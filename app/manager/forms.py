from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    adress = StringField('', validators=[DataRequired(), Length(7, 10,
                                                                message='Wpisz poprawny adress')],
                         render_kw={"placeholder": "Wpisz adress parkingu"})
    number_of_parkings = IntegerField('', validators=[DataRequired(),
                                                      Length(9, 9, message='Wpisz prawidłowe dane')],
                                      render_kw={"placeholder": "Wpisz ilość miejsc na parkingu"})
    name = StringField('', validators=[DataRequired(), Length(3, 20)],
                       render_kw={"placeholder": "Wpisz nazwe parkingu"})

    description = StringField('', validators=[DataRequired(), Length(3, 200)],
                              render_kw={"placeholder": "Wpisz opis parkingu"})
    localisation = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Wpisz współrzędne"})
    submit = SubmitField('Zarejestruj')
