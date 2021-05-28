from . import reservation
from flask import *
from app import db
from flask import render_template, redirect, request, url_for
from flask_login import login_required
from app import models
from ..decorators import admin_required
from .forms import ReservationForm, CalendarForm
from flask_login import login_required, \
    current_user
from app import alcorythm
from ..models import Parking_reservation, otwarcia_history
from ..alcorythm import alcorythm
from sqlalchemy import or_
from datetime import date, datetime, timedelta
import time
def numbers_of_free_parkings():
    list2 = []
    x = models.Parking.query.all()
    for lennik in x:
        list2.append(lennik.id)
    for i in list2:
        d = models.Parking_sensor_id.query.filter_by(parking_id=i).filter(models.Parking_sensor_id.dist <= 20).count()
        parking = models.Parking.query.filter_by(id=i).first()
        parking.number_of_free_parkings = d
    db.session.commit()
    return True

@reservation.route('/', methods=["GET", "POST"])
@login_required
def index():
    x = models.Parking.query.all()
    qq = numbers_of_free_parkings()
    if request.method == 'POST':
        return redirect(url_for('reservation.search', data=request.form["query"]))
    return render_template('panel_Reservation_list.html', people=x)


@reservation.route('/search/<data>', methods=["GET", "POST"])
@login_required
def search(data):
    wynik = None
    numbers_of_free_parkings()
    if request.method == 'POST':
        return redirect(url_for('reservation.search', data=request.form["query"]))
    if not data == '':
        x = models.Parking.query.filter(
            or_(models.Parking.name == data, models.Parking.adress == data,
                models.Parking.description == data)).all()
        wynik = True
    if x == []:
        return redirect(url_for('reservation.index'))
    else:
        return render_template('panel_Reservation_list.html', people=x, wynik=wynik)


@reservation.route('/one/<id>/', methods=['POST', 'GET'])
@login_required
def parking_reservation(id):
    form = ReservationForm()
    calendar = CalendarForm()
    wynik = None
    dzisiaj = date.today().strftime("%Y-%m-%d")
    data = date.today().strftime("%Y-%m-%d")
    nazwa_dnia = date.today().strftime("%A")
    s = data
    d = datetime.strptime(s, '%Y-%m-%d') + timedelta(days=14)
    d = d.strftime('%Y-%m-%d')
    if calendar.validate and calendar.submit2.data:
        date_reservation = request.values.get("trip-start")
        return redirect(url_for('reservation.parking_reservation_confirm', id=id, dzien=date_reservation))
    if form.validate and form.submit.data:
        x = dzisiaj + ' ' + form.end_time_reservation.data
        y = dzisiaj + ' ' + form.start_time_reservation.data
        print(x, y)
        if not alcorythm.alcorythm_reservation(id, y, x) or x == y:
            wynik = True
        else:

            reservation = Parking_reservation(user1_id=current_user.id, parking_id=id, date_reservation=dzisiaj,
                                              start_time_reservation=form.start_time_reservation.data,
                                              end_time_reservation=form.end_time_reservation.data, status=0)
            db.session.add(reservation)
            db.session.commit()
            return redirect(url_for('reservation.parking_reservation_confirm', id=id, dzien=data))
    return render_template('panelUserkalendarz.html', id=id, form=form, wynik=wynik, data=data, d=d, calendar=calendar,
                           dzisiaj=dzisiaj, nazwa_dnia=nazwa_dnia)


@reservation.route('/one/<id>/<dzien>', methods=['POST', 'GET'])
@login_required
def parking_reservation_confirm(id, dzien):
    form = ReservationForm()
    calendar = CalendarForm()
    wynik = None
    nazwa_dnia = datetime.strptime(dzien, '%Y-%m-%d')
    nazwa_dnia = nazwa_dnia.strftime("%A")
    dzisiaj = date.today().strftime("%m-%d-%y")
    data = date.today().strftime("%Y-%m-%d")
    s = data
    d = datetime.strptime(s, '%Y-%m-%d') + timedelta(days=14)
    d = d.strftime('%Y-%m-%d')
    if calendar.validate and calendar.submit2.data:
        date_reservation = request.values.get("trip-start")
        return redirect(url_for('reservation.parking_reservation_confirm', id=id, dzien=date_reservation))

    if form.validate and form.submit.data:
        x = dzien + ' ' + form.end_time_reservation.data
        y = dzien + ' ' + form.start_time_reservation.data
        print(x, y)
        if not alcorythm.alcorythm_reservation(id, y, x) or x == y:
            wynik = True
        else:

            reservation = Parking_reservation(user1_id=current_user.id, parking_id=id, date_reservation=dzien,
                                              start_time_reservation=form.start_time_reservation.data,
                                              end_time_reservation=form.end_time_reservation.data, status=0)
            db.session.add(reservation)
            db.session.commit()
            return redirect(url_for('reservation.parking_reservation_confirm', id=id, dzien=dzien))
    return render_template('panelUserkalendarz.html', id=id, form=form, wynik=wynik, data=data, d=d, calendar=calendar,
                           dzisiaj=dzien, nazwa_dnia=nazwa_dnia)


@reservation.route('/myreservation')
@login_required
def my_reservation():
    list = []
    x = models.Parking_reservation.query.filter_by(user1_id=current_user.id).all()
    d = len(x)
    for i in x:
        baza = models.Parking.query.filter_by(id=i.parking_id).first()
        list.append(baza.name)
        # status=0 - przed rezerwacją
        # status=1 - na parkingu
        # status=2 - zakończone
    return render_template('my_reservation.html', parking=x, d=d, lista=list)


@reservation.route('/deletereservation/<id>')
@login_required
def delete_reservation(id):
    x = models.Parking_reservation.query.filter_by(id=id).first()
    if x.user1_id == current_user.id:
        x = models.Parking_reservation.delete_reservation(id)
        return redirect(url_for('reservation.my_reservation'))




@reservation.route('/opengate/<id>')
@login_required
def open_gate(id):
    reservation = otwarcia_history(parking_id=id, user_id=current_user.id, start=int(time.time() * 1000.0),
                                   end=int((time.time() * 1000.0) + 10000))
    x = models.Parking_reservation.query.filter_by(parking_id=id).first()
    x.status += 1
    db.session.add(reservation)
    db.session.commit()
    return redirect(url_for('reservation.my_reservation'))

@reservation.route('/opengatemobile/<id>')
def open_gate2(id):
    reservation = otwarcia_history(parking_id=id, user_id=0, start=int(time.time() * 1000.0),
                                   end=int((time.time() * 1000.0) + 10000))
    x = models.Parking_reservation.query.filter_by(parking_id=id).first()
    x.status += 1
    db.session.add(reservation)
    db.session.commit()
    return redirect(url_for('reservation.my_reservation'))
