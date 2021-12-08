from .make_dataset import make_dataset, extract_follows_from_users_df, extract_num_followers_from_users_df
import sys
import click

"""
Extract the data required to carry the analysis of hispanic twitch streamers

Usage: 
----------
```
python -m src.data --root_user "ibai" --output_file "data/data.csv" --max_users 10000 --get_follows_of_top 1000 --get_num_followers_of_top 1000
```
"""

@click.command()
@click.option("-o",'--output_file', type=click.Path(),default="data/data.csv",required=False,help="Output (csv) file path")
@click.option('-r', '--root_user', is_flag=False, default="ibai", help="The root user to start the crawl from")
@click.option('-n', '--max_users', is_flag=False, default=20000, help="Maximum number of users to grow the tree for")
@click.option("-in",'--input_df', type=click.Path(),required=False, default=None,
    help="The path of the dataframe to be used to extract the follows or number of followers of this dataset "\
        "according to @get_follows_of_top and @get_num_followers_of_top")
@click.option('-fot', '--get_follows_of_top', default=0, type=int,help="The number of top users to get the follows of by view count")
@click.option('-nfot', '--get_num_followers_of_top', default=0, type=int, help="The number of top users to get the number of followers of by view count")
def main(output_file=None,input_df=None,root_user=None,max_users=None,get_follows_of_top=None,get_num_followers_of_top=None):
    if not input_df:
        make_dataset(root_user,output_file=output_file,max_users=max_users,get_follows_of_top=get_follows_of_top,get_num_followers_of_top=get_num_followers_of_top)
    else:
        if get_follows_of_top:
            extract_follows_from_users_df(input_df,output_file,get_follows_of_top)
        if get_num_followers_of_top:
            extract_num_followers_from_users_df(input_df,output_file,get_num_followers_of_top)
        else:
            raise ValueError("Either get_follows_of_top or get_num_followers_of_top must be specified if input_df is specified")

if __name__ == "__main__":  
    main()