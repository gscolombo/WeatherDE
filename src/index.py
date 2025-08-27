import streamlit as st
import pydeck as pdk
from datetime import timedelta

from app.main import data


st.title("Painel do clima")

brt_offset = timedelta(hours=-3)

temp_data = data[["utc", "lat", "lon", "temp", "local_name"]]
temp_data = temp_data.assign(dt=(temp_data["utc"] + brt_offset)
                             .dt
                             .strftime("%d/%m/%Y, %H:%M:%S"))


st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=-15,
            longitude=-47,
            zoom=4,
            pitch=30
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                temp_data,
                opacity=0.8,
                get_position=["lon", "lat"],
                get_radius=20000,
                get_fill_color=['temp/30 * 255', 50, 0],
                pickable=True,
                extruded=True,
            )
        ],
        tooltip={
            "text": "{local_name}\n{lat}, {lon}\nTemperatura: {temp}°C\nAtualizado em: {dt}"}
    )
)
