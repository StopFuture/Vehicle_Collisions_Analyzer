import streamlit as st
import pydeck as pdk
from ParserXML import *


class DownloadButton:
    def __init__(self, tmp_data, Converter):
        x = st.text_input('Select  a name:', value=Converter.source)
        if x is not "":
            Converter.set_source(x)

            st.button(f" Extract this data as {x}.html ", key=None, help=None,
                      on_click=Converter.create_html(tmp_data, x))


class FinalHtmlCreator:
    def __init__(self, tmp_data, Converter):
        st.button(
        f"Extract original data as  {Converter.set_source(st.text_input('Select a  name: ', value=Converter.source))}.html ",
        key=None, help=None, on_click=Converter.create_html(tmp_data, Converter.source))


class HeatMap:
    def __init__(self, data, midpoint, injured_people):
        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            views=[pdk.View(type="MapView", controller=True)],
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 9,
                "pitch": 1,
            },
            layers=[

                pdk.Layer(
                    "ScatterplotLayer",
                    data=data.query("injured_persons >= @injured_people")[cols],
                    get_position=['longitude', 'latitude'],
                    auto_highlight=True,
                    get_radius=200,  # Radius is given in meters
                    get_fill_color=[255, 0, 0, 150],  # Set an RGBA value for fill
                    pickable=True
                ),
                pdk.Layer(
                    "HeatmapLayer",
                    data=data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"),
                    get_position=['longitude', 'latitude'],
                    auto_highlight=True,
                    opacity=0.05,
                    get_radius=200,  # Radius is given in meters
                    get_fill_color=[255, 'lng > 0 ? 200 * lng : -200 * lng', 'lng', 140],  # Set an RGBA value for fill
                    pickable=True
                ),
            ],
        ))


class HistMap:
    def __init__(self, data, midpoint):
        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            map_provider='carpo',
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 11,
                "pitch": 50,
                "min_zoom": 10,
                "max_zoom": 15,
            },
            tooltip={"html": "<b>Elevation Value:</b> {elevationValue} <br/> ", "style": {"color": "white"}},
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data[['date-time', 'latitude', 'longitude']],
                    get_position=['longitude', 'latitude'],
                    radius=100,
                    extruded=True,
                    pickable=True,
                    elevation_scale=10,
                    elevation_range=[10, 1000],
                    auto_highlight=True,
                    coverage=1,
                ),
            ],
        ))


class Box:
        def __init__(self, data):
            select = st.selectbox('Affected class', ['Pedestrians', 'Cyclists', 'Motorists'])

            k_streets = st.slider("Choose number of streets", 1, 20)

            if select == 'Pedestrians':
                st.table(data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].
                         sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:k_streets])
            elif select == 'Cyclists':
                st.table(data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].
                         sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:k_streets])

            else:
                st.table(data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].
                         sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:k_streets])