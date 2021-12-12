path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

title = 'Network Analysis of Hispanic streamers in the Twitch community'

intro = '''
#  Analysis of Hispanic streamers in the Twitch community

This is a network analysis of the Twitch community of Hispanic streamers.
For this analysis, we have used the [Twitch API](https://dev.twitch.tv/docs/api/reference/) in 
order to get the data about streamers and their followers. 

... 


'''


explanations_of_graph_1 = '''
For the user represented in orange, we get 15 users followed by him and represent among those users how they follow each other.

'''

explanations_of_graph_2 = '''
For the user represented in orange, we extract all the users he follows and compare the followers of those user with the original user represented in orange
'''

references = '''

---
## References and Credit

- Twitch API: https://dev.twitch.tv/docs/api/reference/

- Ana Blanco's ([casiopa](https://github.com/casiopa)) [EDA-IMDb](https://share.streamlit.io/casiopa/eda-imdb/main/src/utils/streamlit/EDA_IMDb_main.py) streamlit app.

'''
