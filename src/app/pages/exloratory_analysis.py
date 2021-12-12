import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

import streamlit as st
from ..constants import *

import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly"

def set_analysis(df):

    st.title('Exploratory Data Analysis of the Twitch `streamers` Dataset')

    
    menu_items = ["View Count - Num Followers"]
    menu_variables= st.radio(
        "",
        menu_items,#"Rating","Metascore", "Presupuesto", "Recaudación", "Beneficios", "ROI"),
    )

    if menu_items.index(menu_variables) == 0:
        with st.spinner("Loading plot..."):
            fig = get_first_plot(df)
            st.plotly_chart(fig,use_container_width=True)

@st.cache(show_spinner=False)
def get_first_plot(df):
    # plt.figure(figsize=(10,10))
    # user = "davimenxpro"
    # is_user = (df.name.str.lower()==user.lower()).head(5000)

    # Plot the graph with logarithmic scale for the number of followers
    fig = px.scatter(df.head(5000), x="num_followers", y="view_count",
                        hover_name="name", log_x=True, log_y=True,#color=is_user,
                        title=f"View count v Number of followers of the top 5000 Twitch Streamers",
                        labels={"num_followers": "Number of followers", "view_count": "View count"}
    )
    # Set figure theme
    fig.update_layout(
            template="plotly_dark",
            title_font_size=18,
            title_font_family="Sans serif",
            title_x=0.5, title_xanchor="center",
            font=dict(
                    family="Sans serif",
                    size=10,
                    color="#ffffff"
            ),
            paper_bgcolor="#222222",plot_bgcolor="#222222",
            legend_title_font_size=12, legend_font_size=12,
            legend_font_color="#ffffff",legend_title_font_color="#ffffff",
            legend_orientation="h",
            legend_x=0.5, legend_xanchor="center", 
            legend_y=1.1, legend_yanchor="bottom",
            height=600,
            width=800,
    )

    return fig

#px.scatter(df.head(5000),x="num_followers", y="view_count",color=is_user,hover_data=["name"])