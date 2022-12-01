from ControlElements.DataImporter import *
import streamlit as st

st.title("📈           Diagrams         ")
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
            data2 = data

            st.header("The total distribution of accidents by the number of vehicles involved")
            bar_example = TotalBarChart(data)

            st.header("Grouping of transport that most often gets into accidents")
            PieChart(data)

            st.header("Most common reasons for accidents")
            BarCauseChart(data)

            st.header("🕑 Correlation in time")
            st.subheader("How many collisions occur during a given time of day(60 min interval)?")

            HourBreak(origin)
            DayBreak(origin)
            MonthBreak()

        except Exception as x:
            x = x
            st.markdown("⚠️   **Go back to the previous page and upload SAI file**")

    else:
        st.markdown("⚠️   **Go back to the previous page and upload SAI file**")


except Exception as x:
    x = x
    st.markdown("⚠️   **Go back to the previous page and upload SAI file**")

