import streamlit as st
import pydeck as pdk
import numpy as np
from folium.plugins import MarkerCluster
import folium as folium
from streamlit_folium import folium_static


@st.experimental_singleton
class HeatMap:
    def __init__(self, data, midpoint, injured_people):
        if injured_people <= 0:
            pass

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
                    data=data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"),
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


@st.experimental_singleton
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


@st.experimental_singleton
class GroupMap:
    def __init__(self, tmp_data):
        midpoint = (np.average(tmp_data["latitude"].dropna(how="any")),
                    np.average(tmp_data["longitude"].dropna(how="any")))
        # s = '''
        if "group_map" not in st.session_state:
            st.session_state["group_map"] = None

        if st.session_state["group_map"] is None:
            group_map = folium.Map(location=[midpoint[0], midpoint[1]], tiles='Stamen Toner',
                                   zoom_start=10)
            st.session_state["group_map"] = group_map
            mc = MarkerCluster()

            for each in tmp_data.iterrows():
                mc.add_child(folium.Marker(location=[each[1]['latitude'], each[1]['longitude']]))

            group_map.add_child(mc)
            st.session_state["group_map"] = group_map

        folium_static(st.session_state["group_map"])
        st.markdown("Note: Points are clustered via the **Folium** library.")
