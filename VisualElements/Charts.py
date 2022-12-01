import streamlit as st
from ControlElements.ParserXML import *
import plotly.express as px


class TotalBarChart:
    def __init__(self, data):
        data2 = data
        vh_type = ["vehicle_type_1", "vehicle_type_2", "vehicle_type_3", "vehicle_type_4", "vehicle_type_5"]
        group_by_num_vh = dict()

        cnt = 0
        for name in vh_type[::-1]:
            er = name[-1]
            group_by_num_vh[er] = data[name].count() - cnt
            cnt += group_by_num_vh[er]
        self.number = cnt
        df = pd.DataFrame(group_by_num_vh.items(),
                          columns=['Number of Vehicles ', 'Number of Accidents '])
        # fig = px.pie(df, values='Number of Accidents ', names='Number of Vehicles ',
        #             color_discrete_sequence=px.colors.sequential.Rainbow)
        fig = px.bar(df, x='Number of Accidents ', y='Number of Vehicles ',
                     color_discrete_sequence=px.colors.sequential.Peach_r)
        st.write(fig)

        original_title = '<p style="font-family:Courier; color:#FF5F1F; font-size: 16px; display:inline;">31995</p>'
        st.markdown(original_title + " – processed cases", unsafe_allow_html=True)

        if st.checkbox("Show raw data", False):
            st.subheader('Raw Data')
            st.write(data2[["date-time", "latitude", "longitude", "location",
                            "vehicle_type_1", "vehicle_type_2", "vehicle_type_3",
                            "vehicle_type_4", "vehicle_type_5"]].head(10))


class BarCauseChart:
    def __init__(self, data):
        cause_of_collision = data.dropna(subset=["contributing_factor_vehicle_1"])
        cause_of_collision = cause_of_collision[["contributing_factor_vehicle_1"]]

        cause_of_collision = pd.DataFrame(cause_of_collision.value_counts(), columns=["Quantity of occurrences"])
        cause_of_collision = cause_of_collision.reset_index(level=[0])
        cause_of_collision.rename(columns={"contributing_factor_vehicle_1": "Contributing Factor"}, inplace=True)
        cause_of_collision.drop(1, inplace=True)

        fig = px.bar(cause_of_collision.head(8), x='Contributing Factor', y='Quantity of occurrences',
                     color_discrete_sequence=px.colors.sequential.Rainbow,
                     title="Factors causing the most number of accidents")
        fig.update_layout(
            title={
                'text': "Factors causing the most number of accidents",
                'x': 0.5,
                'xanchor': 'center'
            })
        st.write(fig)
        if st.checkbox("Show all types ", False):
            st.subheader('Data')
            st.write(cause_of_collision)
        st.markdown("**Analysis:**")
        st.code("Driver Distraction is by far the most common factor leading to accidents\n "
                "on the roads of New York City. "
                "This is a strong argument in favor of the\n promotion of self-driving cars to make our roads safer.",
                language="c++")


class PieChart:
    def __init__(self, data):
        original_title = '<p style="font-family:Courier; color:Gold; font-size: 16px; display:inline;">22391</p>'

        st.write(original_title + " entries are not displayed on the chart, "
                                  "due to the fact that they do not specify the type of car, "
                                  "but only 'Passenger Vehicle'.", unsafe_allow_html=True)
        data_v1 = data[["vehicle_type_1"]]

        grouped = data_v1.value_counts()
        unique_vehicle = pd.DataFrame(grouped, columns=["Quantity of occurrences"])
        unique_vehicle = unique_vehicle.reset_index(level=["vehicle_type_1"])
        unique_vehicle = unique_vehicle.rename(columns={"vehicle_type_1": "Vehicle Type"})
        unique_vehicle1 = unique_vehicle.drop(0)
        unique_vehicle1 = unique_vehicle1.drop(6)

        fig = px.pie(unique_vehicle1.head(10), values='Quantity of occurrences', names='Vehicle Type',
                     color_discrete_sequence=px.colors.sequential.Sunsetdark)
        st.write(fig)
        st.write("To improve visual perception, the diagram shows only 10 types of transport,"
                 " you can view the entire list below")
        if st.checkbox("Show all 68 types ", False):
            st.subheader('Data')
            st.write(unique_vehicle)


class LineChart:
    def __init__(self):
        df1 = pd.read_csv("Datasets/StrategyComp.csv")
        names = df1.columns
        df2 = pd.DataFrame(df1, columns=names)
        parse_strategy = ["XML Dict Strategy", "Element Tree Strategy", "Untangle Strategy"]
        for name in parse_strategy[:-1]:
            df2[name] = df2[name] / 100
        df2["Untangle Strategy"] = df2["Untangle Strategy"] / 150
        plot = df2.plot.line(y=parse_strategy, x="N_rows")
        plot.set_title('XML Parse Comparing')
        plot.set_ylabel("Time (s)")
        plot.set_xlabel("Number of records")
        fig = plot.get_figure()
        self.fig = fig

