from ControlElements.Contol_Initialize import *
import time
import streamlit as st
import streamlit as st
import pydeck as pdk
import numpy as np
from folium.plugins import MarkerCluster
import folium as folium
from streamlit_folium import folium_static


cols = ["date-time", "borough", "zip_code", "latitude", "longitude", "location", "on_street_name",
        "cross_street_name", "off_street_name", "injured_persons", "killed_persons", "injured_pedestrians",
        "killed_pedestrians", "injured_cyclists", "killed_cyclists", "injured_motorists",
        "killed_motorists", "vehicle_type_1", "vehicle_type_2", "vehicle_type_3",
        "vehicle_type_4", "vehicle_type_5", "contributing_factor_vehicle_1"]


class DownloadButton:
    def __init__(self, tmp_data, Converter):

        x = st.text_input('Select  a name:', value="")

        st.button(f" Extract this data as {x}.html ", key=None, help=None,
                  on_click=Converter.create_html(tmp_data, x))


class FinalHtmlCreator:
    def __init__(self, tmp_data, Converter):
        x = st.text_input('Select a  name: ', value="")
        st.button(f"Extract original data as  "
                  f"{x}.html ",
                  key=None, help=None, on_click=Converter.create_html(tmp_data, x))


class StarterInit:
    def __init__(self):
        if "source_file" not in st.session_state:
            st.session_state["source_file"] = None
        if "upload_xml" not in st.session_state:
            st.session_state["upload_xml"] = "upload_xml"
        if "upload_check" not in st.session_state:
            st.session_state["upload_check"] = "upload_check"
        if "imported" not in st.session_state:
            st.session_state["imported"] = None


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


class StrategyTester:
    def __init__(self, source_file):
        parse_strategy = st.radio("Choose parse strategy:",
                                  ("XML Dict Strategy", "Untangle Strategy", "Element Tree Strategy"))
        # source_file = st.session_state["source_file"]

        if parse_strategy == "Element Tree Strategy":

            now1 = time.time()  # time object
            context_t = DefParserXML(ElementTreeStrategy())
            context_t.strategy = ElementTreeStrategy()
            imported = context_t.extract_data(source_file)

            now2 = time.time()
            now = now2 - now1

            st.markdown(f"Used time = Parsing + Uploading to web = {round(now, 3)} seconds")
        elif parse_strategy == "Untangle Strategy":

            now1 = time.time()  # time object
            context_t = DefParserXML(UntangleStrategy())
            context_t.strategy = UntangleStrategy()
            imported = context_t.extract_data(source_file)

            now2 = time.time()
            now = now2 - now1

            st.markdown(f"Used time = Parsing + Uploading to web = {round(now, 3)} seconds")
        else:
            now1 = time.time()  # time object
            context_te = DefParserXML(XMLDictStrategy())
            context_te.strategy = XMLDictStrategy()

            imported = context_te.extract_data(source_file)

            now2 = time.time()
            now = now2 - now1

            st.markdown(f"Used time = Parsing + Uploading to web = {round(now, 3)} seconds")
