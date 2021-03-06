from dataclasses import dataclass, field
from .twitch_utils import connect_to_twitch_endpoint

from typing import List, Optional, Union
from functools import lru_cache

from pandas import isnull
import pandas as pd

@dataclass
class User:
    id: str = None
    name: str = None
    num_followers: int = None
    broadcaster_type: str = None 
    description: str = None
    lang: str = None
    last_game_played_name: str = None
    view_count: int = 0 
    profile_image_url: str = None
    created_at: str = None
    user_follows : list = None

    def __hash__(self):
        # Used for storing users in a set. Uniqueness is checked by id
        return hash(self.id)
    
    def __repr__(self):
        # to be used in debugging or displaying the object
        return f"User(name={self.name}, id={self.id}, created_at={self.created_at}, view_count={self.view_count}, num_followers={self.num_followers})"

    def __eq__(self, __o: object) -> bool:
        # Compares if two users are the same based on their id
        if isinstance(__o, User):
            return self.id == __o.id
        return False
    
    def __lt__(self, other):
        # Used for sorting users by their view count
        if isinstance(other, User):
            return self.view_count < other.view_count
        raise TypeError("Cannot compare User to {}".format(type(other)))        

    @property
    @lru_cache()
    def follows(self):
        """
        (cached property) Returns a list of all users this user follows 
        """
        if not isnull(self.user_follows):
            return self.user_follows
        self.user_follows = User.get_user_follows(self)
        return self.user_follows
    
    def get_follows(self):
        """
        Returns a list of all users this user follows
        """
        if not isnull(self.user_follows):
            return self.user_follows
        return self.follows

    @staticmethod
    @lru_cache()
    def get_user_follows(user_or_id:Union[object,str]):
        """
        Returns a list of User objects that the given user follows.

        Parameters:
        -----------
            user_or_id: The user's id as a string or a User object to get the follows of.
        """
        if isinstance(user_or_id, User):
            user_id = user_or_id.id
        else:
            user_id = user_or_id
        try:
            follows_from_resp = connect_to_twitch_endpoint(
                "users/follows", params=dict(from_id=user_id, first=100))
        except Exception as e:
            print(e)
            return []
        follows = [follow["to_id"]
                    for follow in follows_from_resp.get("data")]
        while follows_from_resp.get("pagination"):
            try:
                cursor = follows_from_resp.get(
                    "pagination", dict()).get("cursor")
                if cursor:
                    follows_from_resp = connect_to_twitch_endpoint(
                        "users/follows", params=dict(from_id=user_id, first=100, after=cursor))
                    follows = follows + [follow["to_id"]
                                            for follow in follows_from_resp["data"]]
                else:
                    break
            except Exception as e:
                print(e)
                break
        return follows
    
    def get_num_followers(self):
        if not isnull(self.num_followers):
            return self.num_followers
        self.num_followers = User.get_num_followers_of_user(self)
        return self.num_followers

    @staticmethod
    @lru_cache()
    def get_num_followers_of_user(user_or_id:Union[object,str]):
        """
        Returns the number of followers of the User object or the user with the given id.

        Parameters
        ----------
        user_or_id : Union[User,str]
            The user object or the user's id to get the number of followers of.
        """
        if isinstance(user_or_id, User):
            user_id = user_or_id.id
        else:
            user_id = user_or_id
        follows_resp = connect_to_twitch_endpoint(
            "users/follows", params=dict(to_id=user_id))
        num_followers = follows_resp.get("total")
        return num_followers
    
    @staticmethod
    def get_users(user_ids: list = None, user_names: list = None):
        """
        Uses a list of user ids or names to retrieve the user's data
        and return a list of new User objects.
        """
        if user_names:
            user_ids = [connect_to_twitch_endpoint(
                "users?login="+name)["data"][0]["id"] for name in user_names]
        users_list = []
        # Get users by 100s
        while len(user_ids) > 0:
            users = user_ids[:100]
            user_ids = user_ids[100:]
            user_ids_str = "&id=".join(users)
            resp_user = connect_to_twitch_endpoint(f"users?id={user_ids_str}")
            user_data = resp_user["data"]
            user_channels_str = "&broadcaster_id=".join(users)
            resp_channel = connect_to_twitch_endpoint(
                f'channels?broadcaster_id={user_channels_str}')
            channel_data = resp_channel["data"]
            for i, user_dict in enumerate(user_data):
                user_name = user_dict.get("display_name")
                user_id = user_dict.get("id")
                created_at = user_dict.get("created_at")
                description = user_dict.get("description")
                broadcaster_type = user_dict.get("broadcaster_type")
                profile_image_url = user_dict.get("profile_image_url")
                view_count = user_dict.get("view_count")
                user_channel_data = [channel for channel in channel_data if channel.get("broadcaster_id") == user_id]
                if user_channel_data:
                    lang = user_channel_data[0].get("broadcaster_language")
                    last_game_played_name = user_channel_data[0].get("game_name")
                else:
                    lang = None
                    last_game_played_name = None                

                user = User(
                    id=user_id,
                    name=user_name,
                    created_at=created_at,
                    broadcaster_type=broadcaster_type,
                    profile_image_url=profile_image_url,
                    description=description,
                    view_count=view_count,
                    lang=lang,
                    last_game_played_name=last_game_played_name
                )
                users_list.append(user)

        return users_list
    
    @staticmethod
    @lru_cache()
    def from_id(user_id=None):
        """
        Use a user id to retrieve the user's data and make a User object.
        """
        if user_id is None:
            raise Exception("No user id or user name provided")
        
        return User.get_users(user_ids=[user_id])[0]
    
    @staticmethod
    @lru_cache()
    def from_name(user_name=None):
        """
        Use a user name to retrieve the user's data and make a User object.
        """
        if user_name is None:
            raise Exception("No user id or user name provided")
        
        return User.get_users(user_names=[user_name])[0]

    
    @staticmethod
    def from_df(df):
        """
        Returns a list of User objects from a pandas dataframe.
        """
        users_list = []
        for i, row in df.where(pd.notnull(df), None).iterrows():
            user = User(
                id=row["id"],
                name=row["name"],
                created_at=row["created_at"],
                description=row["description"],
                view_count=row["view_count"],
                lang=row["lang"],
                last_game_played_name=row["last_game_played_name"],
                profile_image_url=row["profile_image_url"],
                broadcaster_type=row["broadcaster_type"],            
                user_follows=row["user_follows"],    
            )
            users_list.append(user)
        return users_list
    
    def retrieve_info(self):
        """
        Uses this object's user id or name to retrieve the user's data
        and updates this object's attributes accordingly.
        """
        if self.id is None and self.name is None:
            raise Exception("No user id or user name attributes have been set")
        if self.id:
            user = User.get_user(user_id=self.id)
        else:
            user = User.get_user(user_name=self.name)
        self.__dict__.update(user.__dict__)
        