import streamlit as st
import pandas as pd
import sys
sys.path.append('.')

from src.app.pages import set_home, set_data, set_analysis, set_graph_analysis
from src.app.constants import *

st.set_page_config(page_title='Twitch Analysis',
                   page_icon='https://www.google.com/s2/favicons?domain=www.twitch.com',
                   layout="wide")

st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Twitch_logo.svg/2560px-Twitch_logo.svg.png', 
    use_column_width=True
)

st.sidebar.header(title)
st.sidebar.markdown('Streamlit Dashboard to explore our analysis of Twitch')


menu = st.sidebar.radio(
    "",
    ("Introduction", "Data", "Exploratory Analysis", 'Graph Analysis','Reproducibility'),
)

# Radio button on the sidebar so that it can be seen everywhere
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write(sidebar_text)

hide_streamlit_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
"""
st.markdown(hide_streamlit_menu_style, unsafe_allow_html=True)

data_path = "data/streamers_small.feather"

@st.cache(persist=True, show_spinner=False)
def load_data():
    df = pd.read_feather(data_path)
    return df

df = load_data()

if menu == 'Introduction':
    set_home()
elif menu == 'Data':
    set_data(df)
elif menu == 'Exploratory Analysis':
    set_analysis(df)
elif menu == 'Graph Analysis':
    set_graph_analysis(df )
else:
    # col1, col2 = st.columns((0.7,0.3))
    st.markdown("## Reproduce our Work")
    st.image("app/main/repo.jpeg", use_column_width=True)
    st.markdown(reproducibility_text)