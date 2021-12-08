# -*- coding: utf-8 -*-
import click
import os, logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import numpy as np

from ..user import User

import logging
# Set the logger format to show the name, time in minutes, and message
logging.basicConfig(
    format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s: %(message)s',
    datefmt='%b %d %H:%M',
    level=logging.INFO
)
logger = logging.getLogger(os.path.basename(__name__).split(".")[-1])

"""
Extract the data required to carry the analysis of hispanic twitch streamers

Usage: 
----------
```
python -m src.data --output_file "data/data.csv" --max_users 10000 --root_user "ibai" --get_follows_of_top 1000
```
"""

@click.command()
@click.option("-o",'--output_file', type=click.Path(),default="data/data.csv",required=False)
@click.option('-r', '--root_user', is_flag=False, default="ibai", is_eager=True)
@click.option('-n', '--max_users', is_flag=False, default=10000, is_eager=True)
@click.option('-f', '--get_follows_of_top', default=-1, is_eager=True, type=int)
@click.option('-f', '--get_num_followers_of_top', default=-1, is_eager=True, type=int)
def main(root_user="ibai",output_file="data/data.csv",max_users=10000,get_follows_of_top=0,get_num_followers_of_top=0):
    """
    Runs data processing scripts to obtain the data  and save it to the /data directory

    Parameters
    ----------
    root_user : str
        The name of the root user to start the tree from.
    output_file : str
        The name of the output file.
    max_users : int
        The maximum number of users to retrieve.
    get_follows_of_top : int
        The number of top users (by view count) to get the follows of after obtaining the information 
        of all the requested users. If 0 then follows wont be retrieved. If -1 then the follows of all users will be retrieved.
    """
    logger.info(f'making dataset of followers from initial user "{root_user}".')

    # Verify that the directory of output_file exists and if not, create it
    output_file_dir = Path(output_file).parent
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    df = make_data_from_root_user(root_user_name=root_user,output_file=output_file,max_users=max_users)

    if get_follows_of_top:
        only_top = len(df) if get_follows_of_top==-1 else get_follows_of_top
        df = extract_follows_from_users_df(df,output_file=output_file,only_top=only_top)
     
    if get_num_followers_of_top:
        only_top = len(df) if get_num_followers_of_top==-1 else get_num_followers_of_top
        df = extract_num_followers_from_users_df(df,output_file=output_file,only_top=only_top)

    if output_file:
        logger.info(f'writing dataset to output file {output_file}')
        df.drop_duplicates(subset=["id"],keep="first").to_csv(output_file,index=False)

def make_data_from_root_user(root_user_name,output_file=None,max_users=None):
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
        logger.info(f'New users will be fetched until {max_users} users are reached or the program is manually interrupted...')
    else:
        logger.info(f'New users will be fetched until the program is manually interrupted. Use ctrl+c when you wish to stop.')
    # Get the root user
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
            if rand_user.name.lower() == "ibai":
                continue
            # Expand the list of streamers from the follows of the random user
            try:
                user_follows_ids = rand_user.follows
                new_users = User.get_users(user_follows_ids)
            except Exception as e:
                logger.error(f"Error while fetching follows of user {rand_user.name} from the API. Error: {e}")
                continue
            users_with_retrieved_follows.append(rand_user)
            users = list(set(users).union(set(new_users)))
            # Remove users that are not in Spanish streamers
            users = [user for user in users if user.lang == "es" and user.broadcaster_type and user not in users_with_retrieved_follows]
            if itt % 10 == 0:
                logger.info(f"Iteration {itt+1}: {len(users)+len(users_with_retrieved_follows)} users have been retrieved until now.")
                if output_file:
                    logger.info("writing dataset to {}".format(output_file))
                    pd.DataFrame(users_with_retrieved_follows+users)\
                        .drop_duplicates(subset=["id"],keep="first")\
                            .dropna(subset=["broadcaster_type"])\
                                .reset_index(drop=True).to_csv(output_file,index=False)
            itt += 1
        else:
            logger.info(f"max_users reached at iteration {itt}. {len(users)+len(users_with_retrieved_follows)} users were retrieved.")
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping the program..")  
        logger.info(f"A total of {len(users)+len(users_with_retrieved_follows)} users were retrieved. Number of iterations: {itt}")
    
    df =  pd.DataFrame(users_with_retrieved_follows+users)\
            .drop_duplicates(subset=["id"],keep="first")\
                .dropna(subset=["broadcaster_type"])\
                    .reset_index(drop=True)
    if output_file:
        logger.info("writing dataset to file before stopping...")
        df.to_csv(output_file,index=False)
    return df

def extract_follows_from_users_df(df_or_file,output_file=None,only_top=1000,print_every=10):
    """
    Extract the follows from a dataframe of users and returns the same dataframe but with the follows of each user.

    Parameters
    ----------
    df_or_file : pd.DataFrame or str
        The dataframe or the path to the dataframe to be used.
    output_file : str
        The path to the output file.
    only_top : int
        If not None, only the follows of the top {only_top} users will be fetched and returned. Otherwise, all the follows will be fetched.
    """
    if isinstance(df_or_file,str):
        df = pd.read_csv(df_or_file,lineterminator='\n')
    else:
        df = df_or_file
    users_of_df = User.from_df(df.drop_duplicates(subset=['name','id'],keep='first'))
    users_sorted = sorted(users_of_df,key=lambda x: x.view_count if x.user_follows is None else 0,reverse=True)
    only_top = len(users_of_df) if only_top is None or only_top>len(df) else only_top
    logger.info(f'Extracting all the follows of the top {only_top}/{len(df)} users in the dataset (by view count)...')
    try:
        for i,user in enumerate(users_sorted[:only_top]):
            if user.user_follows is None:
                user.get_follows()
            if (i+1) % print_every == 0 or i==0:
                logger.info(f"{i+1}/{only_top} have been processed.")
                if output_file:
                    logger.info("writing dataset to file {}".format(output_file))
                    pd.DataFrame(users_of_df).drop_duplicates(subset=["id"],keep="first").to_csv(output_file,index=False)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping the program..")
    df = pd.DataFrame(users_of_df).drop_duplicates(subset=["id"],keep="first")
    if output_file:
        logger.info("writing dataset to file before stopping...")
        df.to_csv(output_file,index=False)
    return pd.DataFrame(users_of_df)

def extract_num_followers_from_users_df(df_or_file,output_file=None,only_top=1000,print_every=10):
    """
    Extract the number of followers from a dataframe of users and returns the same dataframe

    Parameters
    ----------
    df_or_file : pd.DataFrame or str
        The dataframe or the path to the dataframe to be used.
    output_file : str
        The path to the output file.
    only_top : int
        If not None, only the num followers of the top {only_top} users will be fetched and returned. Otherwise, all the num_followers will be fetched.
    """
    if isinstance(df_or_file,str):
        df = pd.read_csv(df_or_file,lineterminator='\n')
    else:
        df = df_or_file
    users_of_df = User.from_df(df.drop_duplicates(subset=['name','id'],keep='first'))
    users_sorted = sorted(users_of_df,key=lambda x: x.view_count if x.num_followers is None else 0,reverse=True)
    only_top = len(users_of_df) if only_top is None or only_top>len(df) else only_top
    logger.info(f'Extracting all the number of followers of the top {only_top}/{len(df)} users in the given dataframe (by view count)...')
    try:
        for i,user in enumerate(users_sorted[:only_top]):
            if user.num_followers is None:
                try:
                    # Extract the number of followers from the API
                    user.get_num_followers()
                except Exception as e:
                    # If the API fails, continue with the next user
                    if isinstance(e,KeyboardInterrupt):
                        logger.info("KeyboardInterrupt received. Stopping the program..")
                        break
                    logger.error(f"Error while getting the number of followers of {user.name}. Error: {e}")
                    continue
            if (i+1) % print_every == 0 or i==0: # Print the progress every 10 iterations
                logger.info(f"{i+1}/{only_top} have been processed.")
                if output_file: # Write the dataframe to file
                    logger.info("writing dataset to file {}".format(output_file))
                    pd.DataFrame(users_of_df).drop_duplicates(subset=["id"],keep="first").to_csv(output_file,index=False)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping the program..")
    df = pd.DataFrame(users_of_df).drop_duplicates(subset=["id"],keep="first")
    if output_file:
        logger.info("writing dataset to file before stopping...")
        df.to_csv(output_file,index=False)
    return df


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
