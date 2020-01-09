import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import time
import streamlit as st

def micro_view(data):
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

        st.subheader("Below is the seasonal grade for %s: for all year" % selected_lake)
        #year = st.slider("Selected year",min_value=2004, max_value=2014, step=1)
        #if year:
        grade_df = new_df[['seasonal.grade']]
        replace_nums = {"A": 5, "B": 4,"C":3,"D":2,"E":1,"F":0}
        grade_df["num_grade"] = grade_df["seasonal.grade"].replace(replace_nums)
        grade_df['Y'] = grade_df.apply(lambda x: 0.5, axis=1)
        layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           width = 900,
                           height = 300,
                           yaxis = dict(range = [0,1],
                                        showticklabels=False,
                                        showgrid=False),
                           xaxis = dict(tickmode = 'linear',
                                        tick0 = grade_df.index.min(),
                                        dtick = 1,
                                        showgrid=False
                                       ))

        colorsIdx = {'A': 'rgb(17,84,23)',
                     'B': 'rgb(21,159,34)',
                     'C': 'rgb(143,179,24)',
                     'D': 'rgb(238,144,21)',
                     'E': 'rgb(238,79,21)',
                     'F': 'rgb(255,44,44)'}
        textIdx = {'A':'A',
                   'B':'B',
                   'C':'C',
                   'D':'D',
                   'E':'E',
                   'F':'F'}

        cols = grade_df['seasonal.grade'].map(colorsIdx)
        texts = grade_df['seasonal.grade'].map(textIdx)

        fig2 = go.Figure(layout = layout)
        fig2.add_trace(
            go.Scatter(mode='markers+text',
                       x=grade_df.index,
                       y=grade_df.Y,
                       hovertemplate = "Year: %{x}",

                       marker=dict(
                           size=45,
                           color = cols),
                       showlegend=False,
                       text = texts,
                       textposition="bottom center",
                       textfont=dict(family="sans serif",
                                     size=23,
                                     color="purple")))
        st.plotly_chart(fig2)
        # st.text("The  seasonal grade for %s is %s" % (selected_lake, grade_df['seasonal.grade'].values))

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

    selected_ws = st.selectbox('Select the watershed you would like to examine:', data["MAJOR_WATERSHED_y"].unique())
    st.subheader("Below are the lakes in {} watershed for each year".format(selected_ws))

        # if selected_ws:
        #     new_dfws = data[data["MAJOR_WATERSHED_y"] == selected_ws].set_index("seasonal.grade")
        #     new_dfws = new_dfws.sort_index(axis=0)

        #     fig3 = px.scatter(new_dfws, x="rec.avg", y="physical.avg", animation_frame="Year", animation_group="LAKE_NAME_x",text="LAKE_NAME_x",
        #     color=new_dfws.index, hover_name="LAKE_NAME_x",size_max=10,
        #     range_x=[0,5.5], range_y=[0,5])
        #     fig3.update_layout(transition = {'duration': 4000})
        # st.plotly_chart(fig3)

    if selected_ws:
        new_dfws = data[data["MAJOR_WATERSHED_y"] == selected_ws].set_index("seasonal.grade")
        new_dfws = new_dfws.sort_index(axis=0)
        fig_scatter = px.scatter(new_dfws,y=new_dfws.index,
        opacity=0.5,
        x = "Number Properties",
        color =new_dfws.index ,
        animation_frame="Year",
        animation_group="LAKE_NAME_x",
        facet_col="COUNTY",
        hover_name="LAKE_NAME_x",
        facet_col_wrap=2)
        
        fig_scatter.update_traces(marker=dict(size=14,
        line=dict(width=2,
        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
        fig_scatter.update_layout(transition = {'duration': 8000})
        fig_scatter.update_xaxes(title_text='')
        fig_scatter.update_layout(
            title="Lake Quality for each year countywise",
            xaxis_title="Number of Properties",
            yaxis_title="Seasonal Grade",
            font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f"
    ))
    st.plotly_chart(fig_scatter)

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

