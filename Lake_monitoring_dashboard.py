import streamlit as st
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots






def main():
    st.markdown(
        """# Data Science Project

    This app displays a water quality monitoring and property report in the Twin Cities Metro Area alongside a machine learning model that produces
    predictions on the future sale value of properties in the area.

    The MCES Citizen-Assisted Monitoring Program (CAMP) \\ The goal of the MCES lake monitoring program is to
    obtain and provide information that enables cities, counties, lake associations, and watershed
    management districts to better manage TCMA lakes, thereby protecting and improving lake
    water quality.
    """
    )
    micro_view()
    macro_view()
    ml_model( )



data_path = "/Data/lake_data_for_viz.csv"

@st.cache
def load_data():
    data = pd.read_csv(data_path)
    return data

data = load_data()

def micro_view():
    selected_lake = st.selectbox('Select the lake you would like to examine:', data["LAKE_NAME_x"].unique())
    if selected_lake:
        new_df = data[data["LAKE_NAME_x"] == selected_lake].set_index("Year")
        new_df = new_df.sort_index(axis = 0)

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        fig.add_trace(
            go.Scatter(x=new_df.index, y=new_df['avg(Total_Phosphorus_RESULT)'], name="Phosphorus Levels"),
            secondary_y=False,)
        fig.add_trace(
            go.Scatter(x=new_df.index, y=new_df['Mean(Secchi_Depth_RESULT)'], name="Secchi Depth Levels"),
            secondary_y=True,)
        # Add figure title
        fig.update_layout(
            title_text="<b>Lake Measurements of %s </b>" % selected_lake,
            legend=go.layout.Legend(
                bgcolor="LightBlue",
                bordercolor="Black",
                borderwidth=1,
            ))
        # Set x-axis title
        fig.update_xaxes(title_text="<b>Year</b>")
        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Phosphorus Levels</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Secchi Depth Levels</b>", secondary_y=True)
        st.plotly_chart(fig)

        st.subheader("Use the slider to check the seasonal grade:")
        year = st.slider("Selected year",min_value=2004, max_value=2014, step=1)
        if year:
            grade_df = data[['Year','LAKE_NAME_y','seasonal.grade']]
            grade_df = grade_df[(grade_df['Year'] == year) & (grade_df['LAKE_NAME_y'] == selected_lake)]
            st.text("The seasonal grade for %s is %s" % (selected_lake, grade_df['seasonal.grade'].values))

        # Plot map
        new_df1 = new_df[['latitude', 'longitude']]
        st.subheader('Geographic data at %s'% selected_lake)
        st.deck_gl_chart(
            viewport={
                'latitude': 44.9773,
                'longitude': -93.2655,
                'zoom': 10,
                'pitch': 50,
             },
             layers=[{
                'type': 'HexagonLayer',
                'data': new_df1,
                'radius': 200,
                'elevationScale': 10,
                'elevationRange': [1000, 1000],
                'pickable': True,
                'extruded': True,
         },     {
                 'type': 'ScatterplotLayer',
                 'data': new_df1,
                 }])
        st.subheader("Median Price of Properties at %s" % selected_lake)
        fig_bar = go.Figure([go.Bar(x=new_df.index, y=new_df['Median(SALE_VALUE)'])])
        fig_bar.update_layout(
            title_text="<b>Median Price of Properties of %s </b>" % selected_lake
            )
        fig_bar.update_xaxes(title_text="<b>Year</b>")
        # Set y-axes titles
        fig_bar.update_yaxes(title_text="<b>Price</b>")

        st.plotly_chart(fig_bar)


def macro_view():
    st.subheader("Average number of properties around major watersheds")
    viz_df1 = data.pivot_table(values='count(PIN)',index='Year',columns='MAJOR_WATERSHED_y').cumsum().reset_index()

    fig = go.Figure(
        layout=go.Layout(
        legend=dict(x=1.2),
        autosize=False,
        width=500,
        height=500,
        xaxis=dict(title='<b>Year</b>',tickmode = 'array',
            tickvals = [2004, 2005, 2006, 2007, 2008, 2009,2010,2011,2012,2013,2014],),
        yaxis=dict(type='log',title='<b>Total Properties</b>'),
        title='<b>Total Number of Properties over time by Major watersheds</b>'))
    fig.update_layout(
        legend=go.layout.Legend(
            bgcolor="LightBlue",
            bordercolor="Black",
            borderwidth=1,
        ))
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['Cannon River'],
                    name="Cannon River",
                    mode="markers+lines",
                    marker=dict(
                        symbol=1,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['Lower Minnesota River'],
                    name="Lower Minnesota River",
                    mode="markers+lines",
                    marker=dict(
                        symbol=2,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['Lower St. Croix River'],
                    name="Lower St. Croix River",
                    mode="markers+lines",
                    marker=dict(
                        symbol=3,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['Mississippi River - Lake Pepin'],
                    name="Mississippi River - Lake Pepin",
                    mode="markers+lines",
                    marker=dict(
                        symbol=4,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['Mississippi River - Twin Cities'],
                    name="Mississippi River - Twin Cities",
                    mode="markers+lines",
                    marker=dict(
                        symbol=5,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['North Fork Crow River'],
                    name="North Fork Crow River",
                    mode="markers+lines",
                    marker=dict(
                        symbol=6,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['Rum River'],
                    name="Rum River",
                    mode="markers+lines",
                    marker=dict(
                        symbol=7,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    fig.add_trace(
        go.Scatter(x=viz_df1['Year'],
                    y=viz_df1['South Fork Crow River'],
                    name="South Fork Crow River",
                    mode="markers+lines",
                    marker=dict(
                        symbol=8,
                        sizemin=2,
                        sizeref=2,
                        size=8,
                        line=dict(color='black', width=1.2)),
                    ))
    st.plotly_chart(fig)

def ml_model():
    st.text("ML here")

if __name__ == "__main__":
    main()
