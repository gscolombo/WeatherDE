from prefect import flow, task
from os import getenv
from dotenv import load_dotenv
from src.data_ingestion.locals import _locals
from requests import get

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

    return {
        d["name"]: {
            "lat": d["lat"],
            "lon": d["lon"]
        }
        for d in data
    }


@task
def fetch_api(coords: dict):
    data = []
    for lat, lon in coords:
        res = get(CURRENTWEATHER_API_URL(lat, lon))
        if (res.ok):
            data.append(res.json())

    return data


@task
def upload_data():
    pass


@flow
def data_ingestion():
    pass


if __name__ == "__main__":
    data_ingestion()
