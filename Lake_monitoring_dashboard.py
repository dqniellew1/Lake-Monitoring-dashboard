import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import time



def main():
    page = st.sidebar.selectbox("Navigate the app", ["Information", "Reports", "Predictions"])
    if page == "Information":
        about()
    elif page == "Reports":
        st.write("# Lakes Water Quality Monitoring Report ⛵️")
        micro_view()
        macro_view()
    elif page == "Predictions":
        ml_model()
    st.sidebar.title(" 🌸 About")
    st.sidebar.info(
        "\nThis app is maintained by [Daniel]("
        "https://www.linkedin.com/in/daniel-lew-1a358bc/) &  [Kapil] (https://www.google.com).\n\n"
    )

data_path = "./Data/lake_data_for_viz.csv"

@st.cache
def load_data():
    data = pd.read_csv(data_path)
    return data
data = load_data()

def about():
    st.markdown("# Lakes Monitoring Dashboard")
    st.markdown(""" This app displays a water quality monitoring and property report in the Twin Cities Metro Area alongside a machine learning model that produces predictions on the future median sale value of properties in the area.

    """)
    st.markdown("**🐳 Data Sources 🐳**")
    st.markdown("This gives a general overview of the data sources "
            "used in this project.")
    st.markdown("* Parcel data")
    st.markdown("This dataset is a compilation of tax parcel polygon and point layers assembled into a common coordinate systems from Twin Cities, Minnesota metropolitan area counties.")
    st.markdown("* Lake monitoring data")
    st.markdown("This dataset contains lake quality data.")
    st.markdown("* MCES data")
    st.markdown("The MCES Citizen-Assisted Monitoring Program (CAMP) - ")
    st.markdown("The goal of the MCES lake monitoring program is to obtain and provide information that enables cities, counties, lake associations, and watershed management districts to better manage TCMA lakes, thereby protecting and improving lake water quality.")
    st.markdown("**🌏 Project Roadmap 🌏**")

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

        st.subheader("Use the slider to check the seasonal grade for %s:" % selected_lake)
        year = st.slider("Selected year",min_value=2004, max_value=2014, step=1)
        if year:
            grade_df = data[['Year','LAKE_NAME_y','seasonal.grade']]
            grade_df = grade_df[(grade_df['Year'] == year) & (grade_df['LAKE_NAME_y'] == selected_lake)]
            st.text("The %s seasonal grade for %s is %s" % (year, selected_lake, grade_df['seasonal.grade'].values))

        # Plot map
        new_df1 = new_df[['latitude', 'longitude']]
        st.subheader(' Geographic data at %s 🌊'% selected_lake)
        st.deck_gl_chart(
            viewport={
                'latitude': 44.9799700,
                'longitude': -93.2638400,
                'zoom': 8,
                'pitch': 50,
             },
             layers=[{
                'type':'PointCloudLayer',
                'data': new_df1,
                'radius': 1500,
                'elevationScale': 80,
                'elevationRange': [800, 10000],
                'pickable': False,
                'extruded': False,
         },     {
                 'type': 'ScatterplotLayer',
                 'data': new_df1,
                 }])
        st.write("# Properties Report 🏣")
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
    st.markdown("""# Predictions 📈

    This portion of the app takes in a json file that have been preprocessed.
    The file is sent to a machine learning model.
    The model then returns the median sale value prediction of a property.
    """)
    st.subheader("Upload json test data here:")
    uploaded_file = st.file_uploader("Choose a json file", type="json")
    if uploaded_file is not None:
        test_data = pd.read_json(uploaded_file)
        test_data_dict = test_data.to_dict(orient='records')
        test_json = json.dumps(test_data_dict)

    if st.button('Run'):
        st.info('Prediction has started, with uploaded file.')
        my_bar = st.progress(0)
        for percent_complete in range(100):
            my_bar.progress(percent_complete + 1)
        url = 'https://guess-model.herokuapp.com/v1/predict/lakePrediction'

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        x = requests.post(url, data = test_json, headers = headers)
        Model_Info = pd.DataFrame.from_dict(x.json())
        st.write("The predictions from the test data gives us a median sale value of  $%s." % Model_Info['predictions'].values)

if __name__ == "__main__":
    main()
