import streamlit as st
import pandas as pd
from requests import get
from os import getenv


from shared.db import DB
from shared.collection import _Collection


def REVERSE_GEOCODING_API_URL(lat: float, lon: float):
    return f" http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={getenv("OPENWEATHER_APPID")}"


@st.cache_resource
def connect_to_db():
    return DB()


db = connect_to_db()


@st.cache_data(ttl=600)
def get_last_records(_db: DB):
    last_records = _Collection("last_main_records", _db).collection.find()
    last_records = list(last_records)
    return last_records


@st.cache_data(ttl=600)
def get_local_name_by_coords(coords: list[tuple[float, float]]):
    local_names = {}
    for lat, lon in coords:
        res = get(REVERSE_GEOCODING_API_URL(lat, lon))

        if res.ok:
            json = res.json()
            local_names[(lat, lon)] = json[0]["local_names"]["pt"]

    df = pd.DataFrame \
        .from_dict(local_names, orient="index", columns=["local_name"]) \
        .reset_index(names="coordinates")

    df[["lat", "lon"]] = pd.DataFrame(
        df["coordinates"].tolist(), index=df.index)

    df = df.drop(columns="coordinates") \
        .set_index(["lat", "lon"])

    return df


data = get_last_records(db)

data = pd.DataFrame.from_dict(data={(d["_id"]["lat"], d["_id"]["lon"], d["dt"]): d["main"]
                                    for d in data}, orient="index").reset_index(names=["lat", "lon", "utc"])

coordinates = data.loc[:, ["lat", "lon"]].to_numpy()
local_names = get_local_name_by_coords(coordinates)

data = data.set_index(["lat", "lon"]).merge(
    local_names, on=["lat", "lon"], how="outer").reset_index()
