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


def get_k_common_followers(filename, filter_weight=0.05, common_followers_with="Ibai"):

    if filename.endswith("csv"):
        df = pd.read_csv(filename, lineterminator='\n')
    elif filename.endswith("feather"):
        df = pd.read_feather(filename)

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

  got_net = Network(height='750px', width='100%',
                    bgcolor='#222222', font_color='white')

  # set the physics layout of the network
  got_net.barnes_hut()

  sources, targets, weigths = df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]

  edge_data = zip(sources, targets, weigths)

  for e in edge_data:
      src = e[0]
      dst = e[1]
      w = e[2]

      got_net.add_node(src, src, title=src)
      got_net.add_node(dst, dst, title=dst)
      got_net.add_edge(src, dst, value=w)

  neighbor_map = got_net.get_adj_list()

  # add neighbor data to node hover data
  for node in got_net.nodes:
      node['title'] += ' Neighbors:<br>' + \
          '<br>'.join(neighbor_map[node['id']])
      node['value'] = len(neighbor_map[node['id']])

  got_net.show_buttons(filter_=['physics'])
  got_net.show(output_file)


def get_top_followers(filename, k=15, common_followers_with="Ibai"):
    '''
    Returns a dataframe with the top k followers of a given user in the network of Twitch streamers.

    Args:
        filename: path to the file with the network of streamers
        k: number of top followers to return
        common_followers_with: name of the user to get the top followers of
    '''

    if filename.endswith("csv"):
        df = pd.read_csv(filename, lineterminator='\n')
    elif filename.endswith("feather"):
        df = pd.read_feather(filename)

    follows_of_user = df.loc[df.name.str.lower(
    ) == common_followers_with.lower()].iloc[0]["user_follows"]

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

