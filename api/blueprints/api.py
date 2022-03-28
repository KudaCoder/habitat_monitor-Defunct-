from flask import Blueprint, jsonify, request, make_response

from api.models import db, Reading, EnvironmentConfig
from comm import redis

from datetime import datetime, time
import json

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/reading/current/")
def reading_current():
    reading = redis.get_redis("reading")
    reading = reading.__dict__
    return jsonify(reading)


@bp.route("/reading/add/", methods=["POST"])
def reading_add():
    data = json.loads(request.json)

    if data["temp"] is None or data["hum"] is None:
        return make_response(jsonify({"error": "Invalid data format!"}))
    
    reading = Reading(temperature=data["temp"], humidity=data["hum"])
    db.session.add(reading)
    db.session.commit()
    return make_response(jsonify({"message": "Reading added successfully!"}), 200)

@bp.route("/reading/list/")
def reading_list():
    reading_dict = Reading.to_dict(Reading.query)
    return jsonify(reading_dict)

@bp.route("/reading/find/period/")
def reading_find_by_period():
    period_data = json.loads(request.json)
    unit = period_data["unit"]
    time = period_data["time"]

    if unit.lower() not in ("minutes", "hours", "days"):
        return make_response(jsonify({"error": "Incorrect unit type"}), 400)
    if isinstance(time, str):
        try:
            time = int(time)
        except Exception:
            return make_response(jsonify({"error": "Incorrect time format"}), 400)
            
    readings = Reading.find(period=f"{unit}={time}")
    reading_dict = Reading.to_dict(readings)
    return make_response(jsonify(reading_dict), 200)
    

@bp.route("/reading/find/range/")
def reading_find_by_range():
    range_data = json.loads(request.json)
    d_from = range_data["dateFrom"]
    d_to = range_data["dateTo"]

    readings = Reading.find(dateFrom=d_from, dateTo=d_to)
    reading_dict = Reading.to_dict(readings)
    return jsonify(reading_dict)


@bp.route("/config/get/")
def config_get():
    env = EnvironmentConfig.query.order_by(EnvironmentConfig.created.desc()).first()
    env_data = EnvironmentConfig.to_dict(env)
    return jsonify(env_data)


@bp.route("/config/new/")
def config_new():
    env = EnvironmentConfig.factory()
    env_data = EnvironmentConfig.to_dict(env)
    return jsonify(env_data)


@bp.route("/config/set/", methods=["POST"])
def config_set():
    env_data = json.loads(request.json)
    env_data["lights_on_time"] = time.fromisoformat(env_data["lights_on_time"])
    env_data["lights_off_time"] = time.fromisoformat(env_data["lights_off_time"])
    env = EnvironmentConfig.factory(**env_data)
    redis.update_redis("environment", EnvironmentConfig.to_dict(env))
    return jsonify({"message": "Config updated successfully!"})
