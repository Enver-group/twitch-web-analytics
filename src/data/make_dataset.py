# -*- coding: utf-8 -*-
import click
import os, logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import numpy as np

from ..user import User

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@click.command()
@click.argument('output_filepath', type=click.Path(),default="data/data.csv",required=False)
@click.option('-r', '--roor_user_name', is_flag=False, default="ibai", is_eager=True)
@click.option('-m', '--max_users', is_flag=False, default=10000, is_eager=True)
def main(roor_user_name="ibai",output_filepath=None,max_users=10000):
    """ Runs data processing scripts to obtain the data  and save it to the /data directory
    """
    logger.info(f'making dataset of followers from initial user {roor_user_name}.')

    make_data_from_root_user(root_user_name=roor_user_name,output_filepath=output_filepath,max_users=max_users)

    if output_filepath:
        logger.info(f'writing dataset to output file {output_filepath}')


def make_data_from_root_user(root_user_name,output_filepath=None,max_users=None,):
    """
    Generate a dataset from a tree of twitch users follows starting from the follows of the given root user until it is manually stopped.

    Parameters
    ----------
    root_user_name : str
        The name of the root user to start the tree from.
    
    Returns
    -------
    pd.DataFrame : list
        A list of all the users in the tree.
    """
    logger.info(f'Collecting users from a tree of twitch users follows starting from the follows of the user: {root_user_name}')
    if max_users:
        logger.info(f'New users will be fetched until {max_users} users are reached or the program is manually interrupted.')
    else:
        logger.info(f'New users will be fetched until the program is manually interrupted. Use ctrl+c when you wish to stop.')
    # Get the root user
    # if os.path.exists(output_filepath):
    #     users_df = pd.read_csv(output_filepath)
    #     if users_df.iloc[0]["name"].lower() == root_user_name.lower():
    #         logger.info(f'found existing dataset at {output_filepath} which will be used to start the tree.')
    #         users = User.from_df(users_df)
    #         root_user = users.pop(0)
    #     else:
    #         root_user = User.from_name(user_name=root_user_name)
    #         users = [root_user]
    # else:
    root_user = User.from_name(user_name=root_user_name)
    assert root_user.lang == "es", "Only Spanish users can be fetched."
    users = [root_user]
    users_with_retrieved_follows = []
    itt = 0
    try:
        logger.info(f"The tree will be expanded randomly starting from the root.")        
        while len(users)>0 and (max_users is None or (len(users)+len(users_with_retrieved_follows))<max_users):
            # Get the next user randomly from the list of users
            rand_user_ind = np.random.randint(0,len(users))
            rand_user = users.pop(rand_user_ind)
            # Expand the list of streamers from the follows of the random user
            user_follows_ids = rand_user.follows
            new_users = User.get_users(user_follows_ids)
            users_with_retrieved_follows.append(rand_user)
            users = list(set(users).union(set(new_users)) - set(users_with_retrieved_follows))
            # Remove the streamers that are not in Spanish
            users = [user for user in users if user.lang == "es"]            
            if itt % 10 == 0:
                logger.info(f"Iteration {itt+1} - {len(users)+len(users_with_retrieved_follows)} users have been retrieved until now.")
                if output_filepath:
                    logger.info("writing dataset to file {}".format(output_filepath))
                    pd.DataFrame(users_with_retrieved_follows+users).drop_duplicates(subset=["id"],keep="first").to_csv(output_filepath,index=False)
            itt += 1
        else:
            logger.info(f"max_users reached. {len(users)+len(users_with_retrieved_follows)} users were retrieved.")
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping the program..")  
        logger.info(f"A total of {len(users)+len(users_with_retrieved_follows)} users were retrieved.")    
    
    df =  pd.DataFrame(users_with_retrieved_follows+users).drop_duplicates(subset=["id"],keep="first").to_csv(output_filepath,index=False)
    if output_filepath:
        logger.info("writing dataset to file before stopping...")
        pd.DataFrame(users_with_retrieved_follows+users).drop_duplicates(subset=["id"],keep="first").to_csv(output_filepath,index=False)
    return df

def extract_follows_from_users_df(df_or_file):
    """
    Extract the follows from a dataframe of users and returns the same dataframe but with the follows of each user.
    """
    if isinstance(df_or_file,str):
        df = pd.read_csv(df_or_file)
    else:
        df = df_or_file
    users_of_df = User.from_df(df.drop_duplicates(subset=['name','id'],keep='first'))
    for user in users_of_df:
        if user.user_follows is None:
            user.get_follows()
    return pd.DataFrame(users_of_df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
