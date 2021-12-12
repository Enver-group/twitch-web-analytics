import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pickle
import collections

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

    st.write(get_df_metrics(df),use_container_width=True)
    st.plotly_chart(get_pie_cores_topusers(df))

@st.cache(show_spinner=False)
def get_df_metrics(df):
    df_ranking_metrics = pd.DataFrame()
    for m in ["indegree","outdegree", "closeness", "betweenness", "pagerank", "nx_cores"]:
        # load metric
        folder_name = "data/fundamental_metrics"
        file_name = f"{folder_name}/{m}.pkl"
        with open(file_name, 'rb') as f:
            metric = pickle.load(f)
        ranking10_ids = list(metric.keys())[:10]
        ranking10_names = [df[df["id"]==node_id]["name"].iloc[0] for node_id in ranking10_ids]
        df_ranking_metrics[m] = ranking10_names
    return df_ranking_metrics

def get_pie_cores_topusers(df):
    df_ranking_metrics = get_df_metrics(df)
    # load k-core descomposition
    with open("data/fundamental_metrics/nx_cores.pkl", 'rb') as f:
        nx_cores = pickle.load(f)
    
    # reformat NetworkX solution
    nx_cores_format = {c:set() for c in set(nx_cores.values())}
    for node in nx_cores:
      nx_cores_format[nx_cores[node]].add(node)

    # order the imporant users (according to fundamental metrics) by core number
    important_users_names = collections.Counter()
    for m in df_ranking_metrics.drop("outdegree", axis=1):
      for user_name in df_ranking_metrics[m]:
        important_users_names.update([user_name,])
    # get keys with highest values counter
    important_users_names = [i[0] for i in important_users_names.most_common()][:11]
    
    # extract ids from important users
    important_users_ids = list(df[df["name"].isin(important_users_names)]["id"])

    important_users_cores = { user_id: nx_cores[user_id] for user_id in important_users_ids}
    # reformat NetworkX solution
    important_users_cores_format = {c:set() for c in set(important_users_cores.values())}
    for node in important_users_cores:
      important_users_cores_format[important_users_cores[node]].add(node)
    important_users_cores_format = dict(sorted(important_users_cores_format.items(), key=lambda x: x[0],reverse=True))

    n_important_users = len(important_users_ids)
    cores = []
    percentage_cores = []
    for core in important_users_cores_format:
      cores.append(core)
      users_in_core = [df[df["id"]==node_id]["name"].iloc[0] for node_id in important_users_cores_format[core]]
      percentage_cores.append(len(users_in_core)/n_important_users)
    
    fig = px.pie(values=percentage_cores, names=list(important_users_cores_format.keys()), 
        title = "K-Core Decomposition in 10 top users")
    fig.update_layout(
            paper_bgcolor="#222222",plot_bgcolor="#222222",
    )
    return fig


@st.cache(show_spinner=False)
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
        df_ = df_.head(n_max).groupby(bar_by).count().reset_index()
        title = f"Count of Streamers by {labels_dict[bar_by]}"
        df_ = df_[df_[bar_of]>5]
    else:
        df_ = df_.head(n_max).groupby(bar_by).sum().reset_index()
        title=f"{labels_dict.get(bar_of)} by {labels_dict.get(bar_by)}"

    for row in df_.iloc:
        cat = row[bar_by]
        top_streamer_in_category = df[df[bar_by]==cat].sort_values(bar_of,ascending=False).iloc[0]['name']
        df_.loc[df_[bar_by]==cat,'Top Streamer'] = top_streamer_in_category

    fig = px.bar(
        df_,
        x=bar_by, y=bar_of,
        color=bar_by,
        hover_data=["Top Streamer"],
        title=title,
        labels={bar_of: labels_dict.get(bar_of), bar_by: labels_dict.get(bar_by)},
        height=600,
        log_y=bar_by in ["last_game_played_name","view_count","num_followers"],
    )
    fig.update_layout(
        paper_bgcolor="#222222",plot_bgcolor="#222222",
    )
    return fig

def get_joins_overtime_plot(df):
    df = df.copy()
    df["month"] = df.created_at.dt.strftime("%Y-%m")
    df["count"] = 1
    df = df.groupby("month").sum().reset_index()
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