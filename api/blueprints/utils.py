from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import pytz
import os

load_dotenv()
API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000/api")


def add_reading(temp=None, hum=None):
    return requests.post(
        f"{API_URL}/reading/add/",
        json=json.dumps(dict(temp=temp,hum=hum))
    ).json()


def list_readings():
    return requests.get(f"{API_URL}/reading/list/")


def find_reading_by_period(unit=None, time=None):
    return requests.get(
        f"{API_URL}/reading/find/period/",
        json=json.dumps({"unit": unit, "time": time})
    ).json()


def find_reading_by_range(dateFrom=None, dateTo=None):
    return requests.get(
        f"{API_URL}/reading/find/range/",
        json=json.dumps({"dateFrom": dateFrom, "daetTo": dateTo})
    ).json()


def get_config():
    return requests.get(f"{API_URL}/config/get/").json()

def new_config():
    return requests.get(f"{API_URL}/config/new/").json()

# TODO: Convert this to use a locale for user
def localise_tz(data):
    if isinstance(data, list):
        for data_point in data:
            data_point = perform_localise(data_point)
    else:
        data = perform_localise(data)
    
    return data

def perform_localise(data):
    for k, v in data.items():
        if isinstance(v, str):
            try:
                tz = pytz.timezone("UTC")
                utc_time = datetime.fromisoformat(v)
                tz_time = tz.localize(utc_time)
                data[k] = tz_time.astimezone(tz=pytz.timezone("Europe/London")).isoformat()
            except Exception:
                # Not an isoformat, just move on
                pass
    return data
