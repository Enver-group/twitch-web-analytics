path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

title = 'Network Analysis of Hispanic streamers in the Twitch community'

intro = '''
#  Analysis of Hispanic streamers in the Twitch community Dashboard

This is a network analysis of the Twitch community of Hispanic streamers.
For this analysis, we have used the [Twitch API](https://dev.twitch.tv/docs/api/reference/) in 
order to get the data about streamers and their followers. The main goals of this analysis are:





-Visualize in detail the Twitch Hispanic Network



-Perform a Community detection analysis




-Make a raking of streaming with various metrics





'''



explanations_of_graph_1 = '''
For the user represented in orange, we get 15 users followed by him and represent among those users how they follow each other.

'''

explanations_of_graph_2 = '''
For the user in orange, we extract all the users he follows and for each of those user we also get all his followers. We compute how similar those two list of followers are and they are represented in the graph if their similarity is greater than 5%
'''


references = '''

---
## References and Credit

- Twitch API: https://dev.twitch.tv/docs/api/reference/

- Ana Blanco's ([casiopa](https://github.com/casiopa)) [EDA-IMDb](https://share.streamlit.io/casiopa/eda-imdb/main/src/utils/streamlit/EDA_IMDb_main.py) streamlit app.

'''
