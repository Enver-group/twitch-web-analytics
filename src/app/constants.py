path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

title = 'Network Analysis of Hispanic streamers in the Twitch community'

# HOME =========================================================================
intro = '''
#  Analysis of Hispanic streamers in the Twitch community

This is a network analysis of the Twitch community of Hispanic streamers.
For this analysis, we have used the [Twitch API](https://dev.twitch.tv/docs/api/reference/) in 
order to get the data about streamers and their followers. 

... 


'''


# DATA =========================================================================

columns_description = '''
### Columns:
- `id`: ID of the Twitch user
- `name`: Display name of the Twitch user
- `num_followers`: Total number of followers of the Twitch user
- `view_count`: Total number of views of the Twitch user
- `broadcaster_type`: Type of broadcaster (partner, affiliate, etc.)
- `description`: Description of the Twitch user in its profile
- `lang`: Language of the Twitch user (They are all spanish)
- `last_game_played_name`: Name of the last game played by the Twitch user as of December 5th, 2021
- `profile_image_url`: URL of the profile image of the Twitch user
- `created_at`: Date when the Twitch user was created
- `user_follows`: List of the ids of the users that the Twitch user follows
'''

how_it_was_extracted = '''
### How it was extracted:
- We start with a single streamer in the Twitch community (Ibai for example) and iteratively extracted all the followers of that user to put them in a set.
- Afterwards we randomly take a user from that set of follows, extract all the followers of said user, and expand the set.
- We repeat this process for random users that are not yet visited until we reach a pre-defined maximum number of users.
- From the information about each user visited, we constructed the `streamers` dataset.
- The network can be represented with a user as a node pointing to each of the users they follow (`user_follows`) to make the edges.

'''


#GRAPH ANALYSIS ================================================================
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
