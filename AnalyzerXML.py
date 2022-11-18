import streamlit as st
# import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from ParserXML import *
from ConverterToHTML import *
from VisualTools import *

__all__ = [st, pd, np, pdk, px]
DATE_TIME = "date/time"
local_path = ""
file_name = "Datasets/50k_cleaned_from_xml.csv"

DATA_URL = local_path + file_name

st.title("Motor Vehicle Collisions Analyzer")


st.markdown("This application is a Streamlit dashboard that can \
            be used to analyze XML-file from the State Automobile Inspection 🚔💥")
st.markdown("🔵     Author: **Andriy Fedorych**")
st.markdown("🟡     GitHub: [**StopFuture**](https://github.com/StopFuture)")

upload_check = False
xml_source_file = st.file_uploader("Upload XML File", type="xml")

if xml_source_file is not None and upload_check is False:
    try:
        context_t = DefParserXML(XMLDictStrategy())
        context_t.strategy = XMLDictStrategy()
        imported = context_t.extract_data(xml_source_file.name)
        Converter = ConverterToHTML(xml_source_file.name)

        @st.cache(persist=True)
        def load_data(imported_data):
            def lowercase(el): return str(el).lower()

            imported_data.rename(lowercase, axis='columns', inplace=True)

            imported_data.dropna(subset=["latitude", "longitude", "injured_persons", "date-time", "on_street_name"],
                                 inplace=True)
            imported_data['date-time'] = pd.to_datetime(imported_data['date-time'], format='%Y-%m-%d %H:%M:%S')
            for name in ["injured_persons", "killed_persons", "injured_pedestrians",
                         "killed_pedestrians", "injured_cyclists", "killed_cyclists", "injured_motorists",
                         "killed_motorists"]:
                imported_data[name] = imported_data[name].astype('int')


            imported_data['latitude'] = imported_data['latitude'].astype('float')
            imported_data['longitude'] = imported_data['longitude'].astype('float')

            return imported_data

        upload_check = True
    except Exception as exp:
        x = exp
        st.markdown("⚠️   ️**The file is not from the SAI system, try upload another file**")
else:
    upload_check = False

if upload_check:

    data = load_data(imported)
    origin = data

    st.header("Where are the most people injured in city?")
    injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 18)
    midpoint = (np.average(data["latitude"].dropna(how="any")), np.average(data["longitude"].dropna(how="any")))

    HeatMap(data, midpoint, injured_people)
    tmp_data = data.query("injured_persons >= @injured_people")[cols]
    if st.checkbox("Show Raw Data ", False):
        st.subheader('Raw Data')
        x = (st.text_input("Number of displayed rows : ", value="1"))
        st.write(tmp_data.head(int(x) if x != "" else 0))

    tmp_data = data.query("injured_persons >= @injured_people")[cols]

    Converter1 = ConverterToHTML(xml_source_file.name)
    DownloadButton(tmp_data, Converter1)

    st.header("How many collisions occur during a given time of day(60 min interval)?")
    hour = st.slider("Hour to look at", 0, 24)
    data = data[data['date-time'].dt.hour == hour]
    st.markdown(f"Vehicle collisions between {hour}:00 and {hour + 1}:00")
    HistMap(data, midpoint)

    if st.checkbox("Show Raw Data", False):
        st.subheader('Raw Data')
        x = (st.text_input("Number of displayed rows: ", value="10"))
        st.write(data.head(int(x) if x != "" else 0))
    Converter2 = ConverterToHTML(xml_source_file.name)
    tmp_data = data
    st.button(
        f"Extract this data as {Converter2.set_source(st.text_input('Select a  name:', value=Converter2.source))}.html  ",
        key=None, help=None, on_click=Converter2.create_html(tmp_data, Converter2.source))

    # Hist
    st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    filtered = data[
        (data['date-time'].dt.hour >= hour) & (data['date-time'].dt.hour <= hour + 1)
    ]
    hist = np.histogram(filtered["date-time"].dt.minute, bins=60, range=(0, 60))[0]
    chart_data = pd.DataFrame({'minute': range(0, 60, 1), 'crashes': hist})
    fig = px.bar(chart_data, x="minute", y="crashes", hover_data=["minute", "crashes"], height=500)

    st.write(fig)
    st.markdown("The data may be inaccurate, because most of the time is rounded up to 5 minutes")

    if st.checkbox("Show raw data", False):
        st.subheader('Raw Data')
        st.write(data.head(10))

    st.header("Top dangerous streets by affected class")
    Box(data)

    st.header("Creating html file from source data")
    Converter3 = ConverterToHTML(xml_source_file.name)
    FinalHtmlCreator(origin, Converter3)
