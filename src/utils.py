import pandas as pd

def remove_outside_follows(df):
    """
    Remove ids from df.user_follows that are not in df.id

    It expects a dataframe with columns id and user_follows
    """
    df_streamers = df.copy()

    if "id" not in df_streamers.columns:
        df_streamers = df_streamers.reset_index()

    # remove those ids in user_follows that are not in df_streamers.id
    df_streamers_exploded = df_streamers.explode("user_follows")
    df_streamers_exploded = df_streamers_exploded[df_streamers_exploded["user_follows"].isin(df_streamers.id)]
    user_follows_arrays = df_streamers_exploded.groupby("id").user_follows.apply(list).reset_index()
    df_streamers = df_streamers.set_index("id")
    df_streamers.loc[user_follows_arrays.id,"user_follows"] = user_follows_arrays.user_follows.values

    # Make those that appear as nan or are not in the index to be empty arrays
    not_in_set_or_null = ~df_streamers.index.isin(user_follows_arrays.id)
    df_streamers.loc[not_in_set_or_null,"user_follows"] =  pd.Series([[]]*not_in_set_or_null.sum()).values

    return df_streamers