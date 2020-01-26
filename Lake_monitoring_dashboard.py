import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import requests
import json

import time
from PIL import Image
import prediction as pred
import reports as rep

global data
def main():
    page = st.sidebar.selectbox("Navigate the app", ["Information", "Reports", "Predictions"])
    if page == "Information":
        about()
    elif page == "Reports":
        st.write("# Lakes Water Quality Monitoring and Taxation Data Report ⛵️")
        rep.micro_view(data)
        rep.macro_view(data)
    elif page == "Predictions":
        pred.ml_model()
    st.sidebar.title(" 🌸 About")
    st.sidebar.info(
        "\nThis app is maintained by [Daniel]("
        "https://www.linkedin.com/in/daniel-lew-1a358bc/) &  [Kapil] (http://kapil.rbind.io/).\n\n"
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
    image = Image.open('./media/lake.png')
    st.image(image, caption='',use_column_width=True)
    st.markdown("**🐳 Data Sources 🐳**")
    st.markdown("This gives a general overview of the data sources "
            "used in this project.")
    st.markdown("* Parcel data")
    st.markdown("This dataset is a compilation of tax parcel polygon and point layers assembled into a common coordinate systems from Twin Cities, Minnesota metropolitan area counties.")
    st.markdown("* Lake monitoring data")
    st.markdown("This dataset contains lake quality in each lake and year.")
    st.markdown("* MCES data")
    st.markdown("[ The MCES Citizen-Assisted-Monitoring-Program(CAMP)](https://metrocouncil.org/Wastewater-Water/Services/Water-Quality-Management/Lake-Monitoring-Analysis/Citizen-Assisted-Monitoring-Program.aspx)")
    #st.markdown("The MCES Citizen-Assisted Monitoring Program (CAMP) - ")
    st.markdown("The goal of the MCES lake monitoring program is to obtain and provide information that enables cities, counties, lake associations, and watershed management districts to better manage TCMA lakes, thereby protecting and improving lake water quality.")
    st.markdown("**🌏 Project Roadmap 🌏**")
    image2 = Image.open('./media/roadmap.png')
    st.image(image2, caption='',use_column_width=True)






if __name__ == "__main__":
    main()
