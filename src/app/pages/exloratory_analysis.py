import matplotlib.pyplot as plt
import pandas as pd

import streamlit as st
from ..constants import *

import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"

labels_dict = {
    'num_followers':'Number of Followers',
    'view_count':'View Count',
    'broadcaster_type':'Broadcaster Type',
    'last_game_played_name':'Game Played'
}

def set_analysis(df):

    st.title('Exploratory Data Analysis of the Twitch `streamers` Dataset')

    col1, _, _, _ = st.columns(4)
    top_n = col1.slider('Top N Streamers',5,500,5)
    fig1, fig2 = get_top_streamers_fig_by(df,by="num_followers",top_n=top_n), get_top_streamers_fig_by(df,by="view_count",top_n=top_n)
    col1,col2 = st.columns(2)
    col1.plotly_chart(fig1)
    col2.plotly_chart(fig2)

    col1, col2 = st.columns(2)
    bar_of = col1.selectbox("Barplot Of",["view_count","num_followers"])
    bar_by = col2.selectbox("Barplot By",["last_game_played_name","broadcaster_type"])
    barplot = get_barplot_of_by_fig(df,bar_of,bar_by)
    st.plotly_chart(barplot,use_container_width=True)

    col1,col2 = st.columns(2)
    col1.plotly_chart(get_scatter_plotly(df),use_container_width=True)
    col2.plotly_chart(get_joins_overtime_plot(df),use_container_width=True)


@st.cache_data(show_spinner=False)
def get_scatter_plotly(df):
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
            # width=800,
    )

    return fig

def get_top_streamers_fig_by(df,by,top_n=20):
    # top n stremers with most follows
    df = df.copy().sort_values(by,ascending=False).head(top_n).sort_values("num_followers")

    fig = px.bar(
        df,x="name",y=by,
        title=f"Top {top_n} Streamers by {labels_dict[by]}",
        labels={by: labels_dict[by],"name": "Name"},
        height=500,
    )

    fig.update_layout(
        paper_bgcolor="#222222",plot_bgcolor="#222222",
    )

    return fig


def get_barplot_of_by_fig(df,bar_of,bar_by,n_max=5000):
    """
    barplot of bar_of by bar_by
    """
    df_ = df.copy()

    if bar_by in ["last_game_played_name","view_count","num_followers"]:
        df_ = df_.head(n_max).groupby(bar_by).count().reset_index().rename(columns={bar_of:"Count"})
        title = f"Count of Streamers by {labels_dict[bar_by]}"
        df_ = df_[df_["Count"]>5]
        ishist = True
    else:
        df_ = df_.head(n_max).groupby(bar_by).sum().reset_index()
        title=f"{labels_dict.get(bar_of)} by {labels_dict.get(bar_by)}"
        ishist = False

    y_label = bar_of if not ishist else "Count"
    for row in df_.iloc:
        cat = row[bar_by]
        top_streamer_in_category = df[df[bar_by]==cat].sort_values(bar_of,ascending=False).iloc[0]['name']
        df_.loc[df_[bar_by]==cat,'Top Streamer'] = top_streamer_in_category

    fig = px.bar(
        df_,
        x=bar_by, 
        y=y_label if not ishist else "Count",
        color=bar_by,
        hover_data=["Top Streamer"],
        title=title,
        labels={y_label: labels_dict.get(y_label,"Count of Streamers"), bar_by: labels_dict.get(bar_by)},
        height=600,
        log_y=bar_by in ["last_game_played_name","view_count","num_followers"],
    )
    fig.update_layout(
        paper_bgcolor="#222222",plot_bgcolor="#222222",
    )
    return fig

def get_joins_overtime_plot(df):
    df = df.copy().assign(
        month=lambda x: x.created_at.dt.strftime("%Y-%m")
    )
    df["count"] = 1
    # agg by month
    df = df[['count', 'month']].groupby('month').sum().reset_index()
    df["cumulative_growth"] = df['count'].cumsum()

    fig = px.bar(
        df,x="month",y="cumulative_growth",
        title="Cumulative # of Streamers that join the platform over time",
        # hover_data=["Top Streamer"],
        labels={"month": "Month", "cumulative_growth": "Cumulative Growth"},
        height=600,
    )

    fig.update_layout(
            paper_bgcolor="#222222",plot_bgcolor="#222222",
    )

    return fig