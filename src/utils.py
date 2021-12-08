import pandas as pd
from ast import literal_eval

def preprocess_streamers_df(df_streamers):
    """
    Preprocesses the streamers dataframe.
    """
    # Remove duplicates and preprocess
    df_streamers = df_streamers.sort_values(["num_followers","view_count"])\
        .reset_index(drop=True).drop_duplicates(subset=['id'],keep='first')\
            .sort_values(["num_followers","view_count"],ascending=False)\
                .astype({"id":str,"created_at":"datetime64"})

    # clean user_follows and convert each list to array
    df_streamers["user_follows"] = df_streamers.user_follows.\
                                    replace("\r", "", regex=True)\
                                        .str.strip().replace("",None)\
                                            .replace(pd.NA,"None")\
                                                .apply(literal_eval)


    # remove those ids in user_follows that are not in df_streamers.id by exploding the dataframe
    df_streamers_exploded = df_streamers.explode("user_follows")
    df_streamers_exploded = df_streamers_exploded[df_streamers_exploded["user_follows"].isin(df_streamers.id)]
    user_follows_arrays = df_streamers_exploded.groupby("id").user_follows.apply(list).reset_index()
    df_streamers = df_streamers.set_index("id")
    df_streamers.loc[user_follows_arrays.id,"user_follows"] = user_follows_arrays.user_follows.values

    # Make those that appear as nan or are not in the index to be empty arrays
    not_in_set_or_null = ~df_streamers.index.isin(user_follows_arrays.id)
    df_streamers.loc[not_in_set_or_null,"user_follows"] =  pd.Series([[]]*not_in_set_or_null.sum()).values

    return df_streamers