from prefect import flow, task
from os import getenv
from dotenv import load_dotenv
from requests import get
import json
from datetime import datetime

from data_ingestion.locals import _locals
from s3 import S3Client


load_dotenv()

API_KEY = getenv("OPENWEATHER_APPID")


def GEOCODING_API_URL(city, country):
    return f" http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}"


def CURRENTWEATHER_API_URL(lat: float, lon: float):
    return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"


@task
def get_coords():
    data = []
    for city, country in _locals:
        res = get(GEOCODING_API_URL(city, country))
        if (res.ok):
            data.append(*res.json())
            continue

    return [(d["lat"], d["lon"]) for d in data]


@task
def fetch_api(coords: dict):
    data = []
    for lat, lon in coords:
        res = get(CURRENTWEATHER_API_URL(lat, lon))
        if (res.ok):
            data.append(res.json())

    return data


@task
def upload_data(data: list):
    t = int(datetime.now().timestamp())
    s3_client = S3Client()

    enc_data = json.dumps(data).encode('utf-8')
    fname = f"weather@{t}"
    s3_client.put_object(getenv("BUCKET_NAME"), fname, enc_data)


@flow
def data_ingestion():
    upload_data(fetch_api(get_coords()))
