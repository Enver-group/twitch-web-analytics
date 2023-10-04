import streamlit as st
from ..constants import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def set_data(df):

    st.title('Data')

    menu_items = ["The Dataset", "The Users"]
    menu_variables= st.radio("",menu_items)
    df_small = df.head(500)
    # Check if user davimenxpro is in the dataset
    if 'davimenxpro' in df['name'].str.lower().values:
        # remove last row if davimenxpro is in the dataset and add a new row with the davimenxpro data
        df_small = df_small.drop(df_small.tail(1).index)
        df_small = pd.concat([df_small, df[df['name'].str.lower() == 'davimenxpro'].iloc[0].to_frame().T], ignore_index=True)
    df_small = df_small.reset_index(drop=True)
    if menu_items.index(menu_variables) == 0:
        st.markdown('## The `streamers` Dataset: ')
        st.markdown('We scraped information about thousands of Twitch streamers in the Hispanic community using the Twitch API '\
        'in order to construct a dataset that would enable us to conduct our analysis. Here\'s how that dataset looks like:')
        cols = ["id","name","num_followers","view_count","broadcaster_type","description","last_game_played_name","lang","profile_image_url","created_at","user_follows"]
        st.write(df_small[cols])
        st.markdown(f'{len(df_small)} entries  |  11 columns')
        col1, col2 = st.columns(2)
        col1.markdown(columns_description)
        col1.markdown(how_it_was_extracted)
        col2.image("reports/figures/data_extraction_tree.png", width=700)
    else:
        # Select number of users to show
        col_n_user, col_sort = st.columns(2)
        n_users = col_n_user.slider('Number of users to show',max_value=len(df_small), step=4,value=100,min_value=0)
        sort_by = col_sort.selectbox('Sort by', ['name', 'num_followers', 'view_count', 'created_at'],index=2)
        if sort_by in ['created_at',"name"]:
            top_streamers = df_small.sort_values(sort_by, ascending=True).head(n_users).copy()
        else:
            top_streamers = df_small.sort_values(sort_by, ascending=False).head(n_users).copy()
        
        for i in range(len(top_streamers)//4):
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f'''
                <a href="https://www.twitch.tv/{top_streamers.iloc[i*4]["name"]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="{top_streamers.iloc[i*4]['profile_image_url']}" width="200" alt="{top_streamers.iloc[i*4]['name']}">
                    <p style="color:darkgrey" >{top_streamers.iloc[i*4]['name']}</p>
                </a>
                ''',unsafe_allow_html=True
            )
            col2.markdown(f'''
                <a href="https://www.twitch.tv/{top_streamers.iloc[i*4+1]["name"]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="{top_streamers.iloc[i*4+1]['profile_image_url']}" width="200" alt="{top_streamers.iloc[i*4+1]['name']}">
                    <p style="color:darkgrey" >{top_streamers.iloc[i*4+1]['name']}</p>
                </a>
                ''',unsafe_allow_html=True
            )
            col3.markdown(f'''
                <a href="https://www.twitch.tv/{top_streamers.iloc[i*4+2]["name"]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="{top_streamers.iloc[i*4+2]['profile_image_url']}" width="200" alt="{top_streamers.iloc[i*4+2]['name']}">
                    <p style="color:darkgrey" >{top_streamers.iloc[i*4+2]['name']}</p>
                </a>
                ''',unsafe_allow_html=True
            )
            col4.markdown(f'''
                <a href="https://www.twitch.tv/{top_streamers.iloc[i*4+3]["name"]}" target="_blank" style="text-align: center; display: block; text-decoration:none" >
                    <img src="{top_streamers.iloc[i*4+3]['profile_image_url']}" width="200" alt="{top_streamers.iloc[i*4+3]['name']}">
                    <p style="color:darkgrey" >{top_streamers.iloc[i*4+3]['name']}</p>
                </a>
                ''',unsafe_allow_html=True
            )

def bars_nmovies_imdb():
    # Número de pelis por año en IMDb
    n_pelis = [12218, 13148, 14105, 14791, 15862, 16412, 17609, 17967, 17819, 17181, 14632, 11842]

    annos = np.arange(2010,2022)

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(13,6.3))

    ax.bar(annos, n_pelis, edgecolor = "none",
        color = ['#777', '#777', '#777', '#777', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#f5c518', '#777', '#444'])

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)

    annos_xticks = annos.astype(str)
    annos_xticks[11] = 'jun\n2021'
    plt.xticks(annos, labels=annos_xticks, fontsize=12)

    # Pintar valores sobre las barras
    for anno, peli in tuple(zip(annos, n_pelis)):
        ax.text(anno, peli+200, '{0:,}'.format(peli).replace(',', '.'), va='bottom', ha = 'center', fontsize = 14, fontweight = 'regular');
    
    return fig


def bars_nmovies(movies):
    plt.style.use('dark_background')

    #prepare data
    nmovies = movies.groupby('year')['year'].count()


    fig, ax = plt.subplots(figsize=(8,3.5))

    ax.bar(nmovies.index.astype(int), nmovies.values, color = '#f5c518', edgecolor = "none")

    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)

    plt.xticks(nmovies.index.astype(int), fontsize=12)

    # Pintar valores sobre las barras
    for anno, peli in tuple(zip(nmovies.index.astype(int), nmovies.values)):
        ax.text(anno, peli+10, '{0:,}'.format(peli).replace(',', '.'), va='bottom', ha = 'center', fontsize = 18, fontweight = 'regular')

    return fig