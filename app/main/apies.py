from flask import *
from app import ma
from app import models
from . import main
from flask_login import login_required
from ..decorators import manager_required
from ..alcorythm import alcorythm
import time



@main.route('/all_parking')
def api_parkings():
    list = []
    all_posts = models.Parking.query.all()
    for parking in all_posts:
        x = {
            "id": parking.id,
            "name": parking.name,
        }
        list.append(x)
    return jsonify(list)

@main.route('/one_parking/<id>')
@login_required
def api_one_parking(id):
    parking = models.Parking.query.filter_by(id=id).first_or_404()

    x = {
        "id": parking.id,
        "user_id": parking.user_id,
        "adress": parking.adress,
        "localisation": parking.localisation,
        "name": parking.name,
        "description": parking.description,
        "number_of_parkings": parking.number_of_parkings,
        "numer_of_free_parking": parking.number_of_free_parkings
    }
    return jsonify(x)


@main.route('/user_parking/<id>')
@login_required
@manager_required
def api_user_parking(id):
    parking = models.Parking.query.filter_by(user_id=id).first_or_404()

    x = {
        "id": parking.id,
        "user_id": parking.user_id,
        "adress": parking.adress,
        "localisation": parking.localisation,
        "name": parking.name,
        "description": parking.description,
        "number_of_parkings": parking.number_of_parkings,
        "numer_of_free_parking": parking.number_of_free_parkings
    }
    return jsonify(x)


@main.route('/parking_reservation/<id>/<day>/')
def parking_reservation_api(id, day):
    reservation = models.Parking_reservation.query.filter_by(parking_id=id, date_reservation=day).all()
    parking = models.Parking.query.filter_by(id=id).first()
    if parking == None:
        abort(404)
    start = str(day) + ' 00:00:00'
    end = str(day) + ' 00:30:00'
    list = []
    if list.append(alcorythm.alcorythm_reservation_max_function(id, start, end, reservation)) == False:
        abort(404)
    x = {
        "id": parking.id,
        "maxparking": parking.number_of_parkings,
        "reservation": list[0]
    }
    print(x)
    return jsonify(x)


@main.route('/opengate/<id>')
def wwapi_user_parking(id):
    parking = models.Parking.query.filter_by(user_id=id).first_or_404()
    sensor = models.otwarcia_history.query.filter_by(parking_id=id). \
        filter(models.otwarcia_history.start <= int(time.time() * 1000.0)).filter(
        models.otwarcia_history.end >= int(time.time() * 1000.0)).count()
    print(sensor)
    if sensor > 0:
        x = {
            "id": parking.id,
            "status": 'True',
        }
    else:
        x = {
            "id": parking.id,
            "status": 'False',
        }
    return jsonify(x)
