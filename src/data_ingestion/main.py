from prefect import flow, task
from os import getenv
from dotenv import load_dotenv
from requests import get
from datetime import datetime as dt

from models import FullWeatherData
from cities import cities

from timeseries import TimeSeries

load_dotenv()

API_KEY = getenv("OPENWEATHER_APPID")
TTL = 60 * 60 * 24 * 31  # Number of seconds in 31 days


def GEOCODING_API_URL(city, country):
    return f" http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}"


def CURRENTWEATHER_API_URL(lat: float, lon: float):
    return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"


coordinates = tuple[float, float]


@task
def get_coords() -> list[coordinates]:
    data = []
    for city, country in cities:
        print(f"Getting coordinates for {city} ({country})...")
        res = get(GEOCODING_API_URL(city, country))
        if (res.ok):
            data.append(*res.json())
            continue

    return [(d["lat"], d["lon"]) for d in data]


@task
def fetch_api(coords: list[coordinates]):
    data = []
    for lat, lon in coords:
        print(f"Retrieving weather data of coordinates {lat}, {lon}")
        res = get(CURRENTWEATHER_API_URL(lat, lon))
        if (res.ok):
            data.append(res.json())

    return data


@task
def upload_data(data: list[FullWeatherData]):
    c = TimeSeries("weather-ts",
                   timeseries={"timeField": "dt",
                               "metaField": "coord",
                               "granularity": "minutes"},
                   expireAfterSeconds=TTL)

    # Convert UNIX timestamp to datetime objects
    for d in data:
        d["dt"] = dt.fromtimestamp(d["dt"])

    res = c.insert(data, FullWeatherData)

    if res.acknowledged:
        print(f"{len(res.inserted_ids)} entries inserted.")


@flow
def data_ingestion():
    upload_data(fetch_api(get_coords()))
