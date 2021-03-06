import streamlit as st
from ..constants import *
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly"
import matplotlib.pyplot as plt
def set_home():

    image_1 = "https://drive.google.com/uc?id=1SV6b0q2TVHUXfcE6IGCXUu_vuhaDaTJK"   
    image2 = "https://drive.google.com/uc?id=1NbdKCD1aXaGhPdhn9bMwK7F0zgLi-Ol7"
    
    st.write(intro, unsafe_allow_html=True)
    

    col1, col2 = st.columns(2)
    with col1:
        st.image(image_1,caption="Graph of top hispanic streamers and how they follow each other", use_column_width=True)
    with col2:
        st.image(image2,caption="Twitch Music Streamers", use_column_width=True)


    st.write(references, unsafe_allow_html=True)