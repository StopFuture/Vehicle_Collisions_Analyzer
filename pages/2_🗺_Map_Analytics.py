from VisualElements.Breakers import *
from ControlElements.Contol_Initialize import *
from VisualElements.Charts import *
from ControlElements.DataImporter import *
from VisualElements.Grouper import *
from VisualElements.Articles import *
from VisualElements.CustomMaps import *
import streamlit as st
import numpy as np

st.title(" 🗺 Map Analytics ")
st.sidebar.success("Select a page above.")
try:
    source_file = st.session_state["source_file"]
    upload_check = st.session_state["upload_check"]
    upload_xml = st.session_state["upload_xml"]
    if upload_check:
        try:
            if upload_xml:
                data = load_data(st.session_state["imported"])

            else:
                data = load_data(st.session_state["imported"])
                data2 = data
                data2 = data2.where(data2['latitude'] != "NaN")
                data2 = data2.where(data2['longitude'] != "NaN")
                data2 = data2.where(data2['location'] != "NaN")
                data2 = data2.where(data2['injured_persons'] != "NaN")
                data = data2

            origin = data

            st.header("Distribution of accidents by zones of occurrence")

            GroupMap(origin)

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

            Converter1 = ConverterToHTML(source_file.name)
            DownloadButton(tmp_data, Converter1)
            # ds
            #data = origin
            st.header("How many collisions occur during a given time of day(60 min interval)?")
            hour = st.slider("Hour to look at", 0, 24)
            data = data[data['date-time'].dt.hour == hour]
            st.markdown(f"Vehicle collisions between {hour}:00 and {hour + 1}:00")
            HistMap(data, midpoint)

            if st.checkbox("Show Raw Data", False):
                st.subheader('Raw Data')
                x = (st.text_input("Number of displayed rows: ", value="10"))
                st.write(data.head(int(x) if x != "" else 0))
            Converter2 = ConverterToHTML(source_file.name)
            tmp_data = data
            x = Converter2.set_source(st.text_input('Select a  name:', value=""))
            st.button(
                f"Extract this "
                f"data as {x}.html  ",
                key=None, help=None, on_click=Converter2.create_html(tmp_data, x))

            st.header("Top dangerous streets by affected class")
            Box(data)

            st.header("Creating html file from source data")
            Converter3 = ConverterToHTML(source_file.name)
            FinalHtmlCreator(origin, Converter3)
        except Exception as x:
            x = x
            st.markdown("⚠️   **Go back to the previous page and upload SAI file**")
    else:
        st.markdown("⚠️   **Go back to the previous page and upload SAI file**")
except Exception as x:
    x = x
    st.markdown("⚠️   **Go back to the previous page and upload SAI file**")
