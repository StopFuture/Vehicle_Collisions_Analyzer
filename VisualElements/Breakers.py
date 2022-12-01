import streamlit as st
from ControlElements.ParserXML import *
import plotly.express as px
import numpy as np


class DayBreak:
    def __init__(self, data):

        st.subheader("Breakdown by day")
        filtered = data[
            (data['date-time'].dt.day != "NaN")
            ]
        hist = np.histogram(filtered["date-time"].dt.day, bins=31, range=(1, 32))[0]
        chart_data = pd.DataFrame({'day': range(1, 32, 1), 'crashes': hist})
        fig = px.area(chart_data, x="day", y="crashes", hover_data=["day", "crashes"], height=600,
                      pattern_shape_sequence=["x"], color_discrete_sequence=px.colors.sequential.Aggrnyl)

        st.write(fig)

        st.code("Most accidents occur at the beginning of the second third of the month, \n"
                "the last days are less important, due to not being presented in each month.",
                language="c")


class MonthBreak:
    def __init__(self):
        st.subheader("Breakdown by month")

        # generated from main dataset
        lst = [3822, 4076, 4359, 3665, 5062, 5807, 5717, 2816, 1582, 1554, 1685, 1635]

        rng = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
        df = pd.DataFrame(zip(rng, lst),
                          columns=['Month', 'Number of Accidents '])
        fig = px.bar(df, y='Month', x='Number of Accidents ',
                     color='Number of Accidents ')
        st.write(fig)

        st.subheader("Analysis:")
        st.markdown("First of all, the result is a bit puzzling, because it was expected that the closer to winter, "
                    "the more accidents should have happened. So there are two possible explanations.")
        original_title = '<p style="font-family:Courier; color:Orange; font-size: 16px; display:inline;">Primary:</p>'
        st.markdown(original_title, unsafe_allow_html=True)

        st.code("There is sampling bias in our dataset, because looking at January, the number\n"
                "of cases increases dramatically compared to 4 months before. Therefore, the \n"
                "sample is not sufficiently filled.",
                language="rust")
        original_title = '<p style="font-family:Courier; color:Yellow; font-size: 16px; display:inline;">Secondary:</p>'
        st.markdown(original_title, unsafe_allow_html=True)

        st.code("We believe that the data correctly represent the entire sample.\n\n"
                "Therefore, in Autumn and Winter, due to unfavorable weather conditions, drivers\n"
                "drive more carefully, and therefore fewer accidents occur.\n\n"
                "This theory perfectly correlates with the main cause of accidents: Inattention\n",
                language="rust")


class HourBreak:
    def __init__(self, data):

        hour = st.slider("Hour to look at", 0, 24)
        st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
        filtered = data[
            (data['date-time'].dt.hour >= hour) & (data['date-time'].dt.hour <= hour + 1)
            ]
        hist = np.histogram(filtered["date-time"].dt.minute, bins=60, range=(0, 60))[0]
        chart_data = pd.DataFrame({'minute': range(0, 60, 1), 'crashes': hist})
        fig = px.bar(chart_data, x="minute", y="crashes", hover_data=["minute", "crashes"], height=500)

        st.write(fig)
        st.markdown("The data may be inaccurate, because most of the time is rounded up to 5 minutes")
