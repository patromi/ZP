from . import auth
from .forms import LoginForm
from ..models import User
from .forms import RegistrationForm, validate_email
from app import db
from ..email import send_email
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
import logging
from app import models
@auth.app_context_processor
def inject_permissions():
    '''wysłanie wszystkich permisji do konstruktora'''
    return dict(Permission=models.Permission)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    '''funkcja odpowiedzialna za logowanie'''
    form = LoginForm()
    user = None
    wynik = False
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('main.index'))
        else:
            print(wynik)
            wynik = True
    # flash('Nieprawidłowa nazwa użytkownika lub hasło.')
    return render_template('login.html', form=form, wynik=wynik)


@auth.route('/logout')
@login_required
def logout():
    '''Wylogowanie'''
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    '''Funkcja odpowiedzialna za rejestracje'''
    form = RegistrationForm()
    if form.validate_on_submit():
        if validate_email(form.email.data):
            flash('Taki email już istnieje!')
        else:
            user = User(email=form.email.data, username=form.firstname.data, password=form.password.data,
                        nrrej=form.nrrej.data, role_id=3, subname=form.subname.data, numerphone=form.numberphone.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, 'Potwierdź swoje konto.',
                       'mail', user=user, token=token)
            login_user(user, True)
            return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    '''Funkcja odpowiedzialna za akcjeptacji tokenów z maila'''
    print('confirmed')
    if current_user.confirmed:
        print('confirmed')
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        db.session.commit()
        print('Potwierdziłeś swoje konto. Dzięki!')
        return redirect(url_for('auth.confirmed'))
    else:
        print('Link potwierdzający jest nieprawidłowy lub już wygasł.')
        return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    '''Sprawdzenie czy uzytkownik potwierdził maila jak nie to tylko /unconfirmed'''
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    '''Jest to strona informująca o braku potwierdzenia maila'''
    logging.info('Tutaj też ')
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    '''Wysłanie ponownie maila'''
    """Do wykorzystania"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Potwierdź swoje konto.',
               'mail', user=current_user, token=token)
    flash('Nowa wiadomość z potwierdzeniem została wysłana.')
    return redirect(url_for('main.index'))


@auth.route('/confirmed')
@login_required
def confirmed():
    '''Potwierdzenie maila'''
    return render_template('confirmed.html')
