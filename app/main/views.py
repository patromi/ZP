from . import main
from flask import *
from app import models
from flask_login import login_required
from flask_login import current_user
from app import db


@main.app_context_processor
def inject_permissions():
    """wysłanie wszystkich permisji do konstruktora"""
    return dict(Permission=models.Permission)


@main.route('/')


def index():

    """strona startowa"""'do zmiany'
    stats = models.Stats.query.filter_by(id=0).first()

    return render_template('index.html',n_parking=stats.number_of_all_parkings, n_of_c = stats.number_of_cities_with_our_parking, n_of_p = stats.number_of_all_parking_places)


@main.route('/user/<user>/', methods=['GET', 'POST'])
@login_required
def user(user):
    """Konto użytkownika"""
    if not int(current_user.id) == int(user):
        return redirect(url_for('main.index'))
    else:

        user = models.User.query.filter_by(id=user).first_or_404()
        if request.method == 'POST':
            if models.User.verify_email(request.form['email']):
                user.email = request.form['email']
            elif not request.form['email'] == '':
                user.email = request.form['email']
            if not request.form['username'] == '':
                user.username = request.form['username']
            if not request.form['subname'] == '':
                user.subname = request.form['subname']
            if not request.form['numerphone'] == '':
                user.numerphone = request.form['numerphone']
            if not request.form['nrrej'] == '':
                user.nrrej = request.form['nrrej']
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        return render_template('User_panel.html', user=user)



@main.route('/favicon.ico')
def icon():
    return redirect('static/favicon.ico')
