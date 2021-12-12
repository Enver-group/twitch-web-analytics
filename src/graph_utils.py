from pyvis.network import Network
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def df_to_nx(df):
    """
    Convert a dataframe of streamer users information with id and user_follows columns into a networkx graph
    """
    G = nx.from_pandas_edgelist(
        df.reset_index().explode("user_follows"),
        source="id",
        target="user_follows",
        create_using=nx.DiGraph()
    )
    if "name" in df.columns.values:
        nx.set_node_attributes(G, name='name', values=df.name.to_dict())
    if "num_followers" in df.columns.values:
        nx.set_node_attributes(G, name='num_followers',
                               values=df.num_followers.to_dict())
    if "view_count" in df.columns.values:
        nx.set_node_attributes(G, name='view_count',
                               values=df.view_count.to_dict())
    return G


def get_k_common_followers(df_or_filename, filter_weight=0.05, common_followers_with="Ibai"):
    '''
    Get the k most common followers of a streamer

    Parameters
    ----------
    df_or_filename : str or pandas dataframe
        The dataframe or filename of the streamer data
    filter_weight : float
        The minimum weight of a follower to be considered
    common_followers_with : str
        The name of the streamer to get the common followers with
    '''

    if isinstance(df_or_filename, str):
        if df_or_filename.endswith("csv"):
            df = pd.read_csv(df_or_filename, lineterminator='\n')
        elif df_or_filename.endswith("feather"):
            df = pd.read_feather(df_or_filename)
    else:
        df = df_or_filename

    df = df.dropna(how='any',
                    subset=['user_follows'])

    follows_of_user = df.loc[df.name.str.lower(
    ) == common_followers_with.lower()].iloc[0]["user_follows"]

    df = df.loc[df['id'].isin(follows_of_user)]

    weigths = [np.round(len(list(set(df['id']).intersection(
        df["user_follows"].values[i])))/len(df), 2) for i in range(len(df))]

    print(len(weigths))
    df1 = pd.DataFrame({
        "source": [common_followers_with]*len(df),
        "target": df["name"],
        "edge_weights": weigths,
    }).reset_index().drop("index", axis=1).sort_values("edge_weights", ascending=False)

    # remove users without common folloers with Ibai
    df1 = df1[df1.edge_weights > filter_weight]

    return df1


def plot_graph_pyVis(df, output_file):
  ''' df needs to contain three columns: starting node, ending node and the edge weigth'''

  net = Network(height='750px', width='100%',
                    bgcolor='#222222', font_color='white', notebook=True)

  # set the physics layout of the network
  net.barnes_hut()

  sources, targets, weigths = df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]

  edge_data = zip(sources, targets, weigths)

  for src,dst,w in edge_data:
      net.add_node(src, src, title=src)
      net.add_node(dst, dst, title=dst)
      net.add_edge(src, dst, value=w)

  neighbor_map = net.get_adj_list()

  # add neighbor data to node hover data
  for node in net.nodes:
      node['title'] += ' Neighbors:<br>' + \
          '<br>'.join(neighbor_map[node['id']])
      node['value'] = len(neighbor_map[node['id']])

  net.show_buttons(filter_=['physics'])
  net.show(output_file)


def get_top_followers(df_or_filename, k=15, common_followers_with="Ibai"):
    '''
    Returns a dataframe with the top k followers of a given user in the network of Twitch streamers.

    Args:
        df_or_filename: dataframe or path to the dataframe file with the network of streamers
        k: number of top followers to return
        common_followers_with: name of the user to get the top followers of
    '''

    if isinstance(df_or_filename, str):
        if df_or_filename.endswith("csv"):
            df = pd.read_csv(df_or_filename, lineterminator='\n')
        elif df_or_filename.endswith("feather"):
            df = pd.read_feather(df_or_filename)
    else:
        df = df_or_filename

    follows_of_user = df.loc[df.name.str.lower() == common_followers_with.lower()].iloc[0]["user_follows"]

    df = df.loc[df['id'].isin(follows_of_user)]

    df = df.dropna(how='any',
                            subset=['user_follows'])

    df = df[:k] if k < len(df) else df

    id_names = dict(zip(df["id"], df["name"].values.tolist()))

    df["followers_id"] = [list(set(df["id"]).intersection(
        df["user_follows"].values[i])) for i in range(len(df))]

    def double(j):
      return id_names[j]

    df["followers_name"] = df["followers_id"].apply(
        lambda x: list(map(double, x)))

    df = df[['name', "followers_name"]]

    df2 = pd.DataFrame({
        "source": [common_followers_with]*len(df),
        "target": df["name"],
        "edge_weigth": 1,

    })

    for row in df.iterrows():
      for j in row[1].followers_name:

          df2 = df2.append(
              {'source': row[1].values[0], 'target': j, 'edge_weigth': 1}, ignore_index=True)

    return df2


def networkx_centrality_measures(df):
    '''
    Returns a dataframe with the centrality measures of the graph from the Graph 
    represented as a pandas dataframe of edges with source and target columns.

    Args:
        df: dataframe with source, target and edge weigth (pandas edgelist)
    '''

    G = nx.from_pandas_edgelist(df, edge_attr=True)
    
    eigenvector_centrality = nx.eigenvector_centrality_numpy(G)

    betweenness_centrality = nx.betweenness_centrality(G)

    degree_centrality = nx.degree_centrality(G)

    degree_coefficient = nx.clustering(G)

    df_centrality_measures = pd.DataFrame({
        "eigenvector":eigenvector_centrality,
        "betweenness":betweenness_centrality,
        "degree":degree_centrality,
        "degree_coefficient":degree_coefficient,
    })

    return df_centrality_measures,G


def draw_graph(G,title=None):
  pos = nx.spring_layout(G)
  nx.draw_networkx(G, pos)
  plt.title(title)
  plt.show()

def from_pandas_to_pyviz_net(df,height="600px",width="600px", emphasize_node=None):
    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df, edge_attr = True)

    if emphasize_node:
        for node in G.nodes:
            if node == emphasize_node:
                G.nodes[node]["color"] = "orange"
            # else:
            #     G.nodes[node]["color"] = "red"

    # Initiate PyVis network object
    streamer_net = Network(
                       height= height,
                       width= width,
                       bgcolor='#222222',
                       font_color='white',
                       notebook=True
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    streamer_net.from_nx(G)

    # Generate network with specific layout settings
    streamer_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )
    return streamer_net

