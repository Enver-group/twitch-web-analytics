import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import plotly.express as px
import plotly.io as pio
import os
import base64
import pickle
import collections

from ..constants import *
from ...graph_utils import get_k_common_followers, get_top_followers, from_pandas_to_pyviz_net

pio.templates.default = "plotly_dark"


# Define list of streamer to visualize in a graph

def set_graph_analysis(df):

    st.title('Graph Analysis of the Hispanic streaming community in Twitch')

    menu_items = ["Network Metrics","PyViz", "Gephi"]
    menu_variables = st.radio(
        "",
        menu_items,
    )
    if menu_items.index(menu_variables) == 0:
        st.subheader("Network Metrics")
        col1, col2 = st.columns((0.7,0.3) )
        col1.write(get_df_metrics(df),use_container_width=True,height=600)
        col2.plotly_chart(get_pie_cores_topusers(df), use_container_width=True,height=600)
        # Multiselect dropdown menu (returns a list)
        streamer_list = df.sort_values("num_followers", ascending=False).name.tolist()

        col1, _, col2 = st.columns((0.3,.1,0.7) )
        selected_streamer = col1.selectbox(
            'Select streamer to show metrics of', streamer_list)
        col1.image(df[df['name'] == selected_streamer]
                        ['profile_image_url'].values[0], width=100)

        col2.subheader('Position in the ranking of fundamental metrics (from 15460 streamers)')
        col2.write(get_metrics_streamer(selected_streamer, df),use_container_width=True,height=600)     
    elif menu_items.index(menu_variables) == 1:
        show_streamers_pyviz_graphs(df)
    else:
        # st.text("Sorry, this feature is not implemented yet")
        show_gephi_graphs()

def pv_static(fig, name='graph'):
    # https://github.com/napoles-uach/stvis
    h1 = fig.height
    h1 = int(h1.replace('px', ''))
    w1 = fig.width
    w1 = int(w1.replace('px', ''))
    fig.show(name+'.html')
    return components.html(
        fig.html, height=h1+30, width=w1+30
    )

def show_streamers_pyviz_graphs(df):
    
    st.subheader("How do streamers follow each other?")
    streamer_list = df.sort_values("num_followers", ascending=False).name.tolist()
    # Multiselect dropdown menu (returns a list)
    selected_streamer = st.selectbox(
        'Select streamer to visualize', streamer_list)
    image_col, _, _, _ = st.columns(4)
    image_col.image(df[df['name'] == selected_streamer]
                    ['profile_image_url'].values[0], width=100)
    
        
    col1, _, col2 = st.columns( (0.45,.1,0.45) )
    col1.subheader('Graph of Common Follows')
    col1.markdown(explanations_of_graph_1)
    col2.subheader('Graph of User Follows')
    col2.markdown(explanations_of_graph_2)
    col1, _, col2 = st.columns( (0.45,.1,0.45) )
    with col1:
        df1 = get_top_followers(
            df.copy(), common_followers_with=selected_streamer)
        net1 = from_pandas_to_pyviz_net(df1, emphasize_node=selected_streamer)
        pv_static(net1, name="reports/graph")

    with col2:
        df2 = get_k_common_followers(
            "data/streamers.feather", common_followers_with=selected_streamer)
        net2 = from_pandas_to_pyviz_net(df2, emphasize_node=selected_streamer)
        pv_static(net2, name="reports/graph2")

    


def show_gephi_graphs():
    image_mapping = {"11. Carola Network Downsampled.png": "https://drive.google.com/file/d/15UYwfW-a4Jl66j8PKWqWbVxAMeQV32v_/view?usp=sharing",
                     "12. Nissaxter Network downsampeld.png": "https://drive.google.com/file/d/1hnw6cczJnbR6ZS8-uVWPFv1z7_4NHTX5/view?usp=sharing",
                     "05. Twitch 30000 followers downsampled.png": "https://drive.google.com/file/d/1itq2yLykr8n0l2nWAnYpz8L-XkU4RHRS/view?usp=sharing",
                     "03. Twitch 100000 followers by views downsample.png": "https://drive.google.com/file/d/1ivRn3VOoNoD8f-_LaViI4odpUZRGx_jK/view?usp=sharing",
                     "04. Twitch 100000 followers downsamled.png": "https://drive.google.com/file/d/1f-aCAXW4RhGf4WJqtA-V6b2vJUSKv_dL/view?usp=sharing",
                     "09. Twitch ASMR dowsampled.png": "https://drive.google.com/file/d/1PQvnT9uolchlgx5KFExtwQGGg_ZMUdFJ/view?usp=sharing",
                     "06. Twitch Just Chatting downsampled.png": "https://drive.google.com/file/d/1PyvyQMP704icQDy3S_lEF4vBD19Ml0JD/view?usp=sharing",
                     "07. Twitch League of Legends downsampled.png": "https://drive.google.com/file/d/1oR3PtAKy8Fwu85VAmU0Ks1NQk8mLJDeh/view?usp=sharing",
                     "08. Twitch Minecraft downsampled.png": "https://drive.google.com/file/d/1m5SNyNe4dsOL3ZBaX-A8qVeAZ5gQema3/view?usp=sharing",
                     "10. Twitch Music downsampled.png": "https://drive.google.com/file/d/160bllFOG2UhrZqCZ8ioPhWlSUa-JQG1f/view?usp=sharing",
                     "02. Twitch partners downsampled.png": "https://drive.google.com/file/d/1tNS8QpjHO_XKFMNnMRoNBUsoNL_U9Dcs/view?usp=sharing",
                     "01. Twitch top 100 streamers downsampled.png": "https://drive.google.com/file/d/1qOLXeuFEFQUGOhbyEVlZpmHSBFZEy-6v/view?usp=sharing"}
    st.subheader('Graphs Made with Gephi')
    # 2 columns showing the images of the graphs generated by Gephi

    images = sorted([img for img in os.listdir('app/main/images') if img.endswith('.png')])
    st.markdown(
        "Click on the images to see them on full resolution or click [here](https://drive.google.com/drive/folders/1sLFmG8H_ccWvvZcTS-vsuiaTParDkmf5)"\
            " to see more.", unsafe_allow_html=True)
    for i in range(len(images)//2):
        col1, col2 = st.columns(2)
        # get the two images from the dictionary
        image_path1, image_path2 = images[i*2:i*2+2]
        name1, name2 = [" ".join(path.replace(".png","").split(' ')[:-1])
                        for path in [image_path1, image_path2]]
        imagefile1, imagefile2 = open(f"app/main/images/{image_path1}", "rb"), open(f"app/main/images/{image_path2}", "rb")
        contents1,contents2 = imagefile1.read(), imagefile2.read()
        data_url1, data_url2 = base64.b64encode(contents1).decode("utf-8"),base64.b64encode(contents2).decode("utf-8")
        imagefile1.close(), imagefile2.close()

        with col1:
            st.markdown(f'''
                <a href="{image_mapping[images[i*2]]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="data:image/gif;base64,{data_url1}" width="600" alt="{name1}">
                    <p style="color:darkgrey" >{name1}</p>
                </a>
                ''',unsafe_allow_html=True
            )
        with col2:
            st.markdown(f'''
                <a href="{image_mapping[images[i*2+1]]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="data:image/gif;base64,{data_url2}" width="600" alt="{name2}">
                    <p style="color:darkgrey" >{name2}</p>
                </a>
                ''',unsafe_allow_html=True 
            )

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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
        title = "K-Core Decomposition of the 10 top users",height=350
    )
    fig.update_layout(
            paper_bgcolor="#222222",plot_bgcolor="#222222",
            margin=dict(t=32, b=0.7, l=0.7, r=0.7)
    )
    return fig

@st.cache_data(show_spinner=False)
def get_metrics_streamer(streamer_name, df):
    streamer_id = str(int(df.loc[df["name"]==streamer_name]["id"]))
    df_position_metrics = pd.DataFrame()
    for m in ["indegree","outdegree", "closeness", "betweenness", "pagerank", "nx_cores"]:
        # load metric
        with open(f"data/fundamental_metrics/{m}.pkl", 'rb') as f:
            metric = pickle.load(f)
        position = list(metric.keys()).index(streamer_id)
        df_position_metrics[m] = [position+1,]
    df_position_metrics.index = [streamer_name,]
    return df_position_metrics
        
