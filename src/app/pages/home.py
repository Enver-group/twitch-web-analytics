import streamlit as st
from ..constants import *
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly"
import matplotlib.pyplot as plt
def set_home():

    # st.header(title)
    # https://drive.google.com/file/d/1fs4-hYjsrRwOjSSMlbzNrftxyjSGNHg0/view?usp=sharing
    image_1 = "https://drive.google.com/uc?id=1SV6b0q2TVHUXfcE6IGCXUu_vuhaDaTJK"
    # image_2 = '/home/simon/Documents/Uni/WebAnalytics/TwitchProject/app/main/images/vew_count_v_num_followers.png'  
    
    #col4, col5, col6, col7, col8 = st.columns(8)
    
    st.write(intro, unsafe_allow_html=True)
    

    col1, col2 = st.columns(2)
    with col1:
        # load image
        # img = plt.imread(image_1)
        # fig = px.imshow(img)
        # st.plotly_chart(fig,use_container_width=True)
        st.image(image_1,caption="Graph of top hispanic streamers and how they follow each other", use_column_width=True)
    # with col2:
    #     st.image(image_2, use_column_width='always')

    st.write(references, unsafe_allow_html=True)