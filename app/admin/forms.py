from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    user_id = IntegerField('', validators=[DataRequired(), Length(1, 4)],
                           render_kw={"placeholder": "Wpisz id zarządcy"})
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


class EditProfileParkingForm(FlaskForm):
    name = StringField('', validators=[DataRequired(), Length(1, 64)])
    user_id = StringField('', validators=[Length(1, 64)])
    subname = StringField('Nazwisko', validators=[
        DataRequired(), Length(1, 64)])
    number_of_parkings = StringField('', validators=[Length(1, 64)])
    description = StringField('', validators=[Length(1, 128)])
    localisation = StringField('', validators=[Length(0, 64)])
    submit = SubmitField('Wyślij')
