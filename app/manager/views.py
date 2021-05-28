from . import manager
from app import db
from flask import render_template, redirect, request, url_for
from flask_login import login_required, \
    current_user
from app import models
from ..decorators import manager_required
from .forms import LoginForm
from app import admin

@manager.route('/me')
@login_required
@manager_required
def parking_index():
    x = models.Parking.query.filter_by(user_id=current_user.id).all()
    return render_template('panel_manager_own_parkings.html', parking=x)


@manager.route('/create/', methods=['GET', 'POST'])
@login_required
@manager_required
def manager_create_parking_panel():
    form = LoginForm()
    if request.method == 'POST':
        parking = models.Parking(user_id=current_user.id, adress=form.adress.data,
                                 number_of_parkings=form.number_of_parkings.data,
                                 name=form.name.data, description=form.description.data,
                                 localisation=form.localisation.data, number_of_free_parkings=0)
        db.session.add(parking)
        db.session.commit()
        admin.views.stats()
        return redirect(url_for('main.index'))
    return render_template('create_parking.html', form=form)


@manager.route('/me/<id>/', methods=['GET', 'POST'])
@login_required
@manager_required
def manager_one_parking(id):
    parking = models.Parking.query.get_or_404(id)
    if request.method == 'POST':
        if not request.form['name'] == '':
            parking.name = request.form['name']
        if not request.form['adress'] == '':
            parking.adress = request.form['adress']
        if not request.form['number_of_parkings'] == '':
            parking.number_of_parkings = request.form['number_of_parkings']
        if request.form['owner'] == '' or not models.Parking.validate_user_id(request.form['owner']):
            print(models.Parking.validate_user_id(request.form['owner']))
        else:
            print(models.Parking.validate_user_id(request.form['owner']))
            parking.user_id = request.form['owner']
        if not request.form["description"] == '':
            parking.description = request.form["description"]
        if not request.form['position'] == "":
            parking.localisation = request.form['position']
        db.session.add(parking)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('Panel_manager_one_parking.html', parking=parking)
