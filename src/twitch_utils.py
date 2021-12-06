import requests
import os
from dotenv import find_dotenv, load_dotenv

from collections import deque

from .user import User

# load .env file
dotenv = find_dotenv()
load_dotenv(dotenv)

# Twitch Authentication params
authURL = 'https://id.twitch.tv/oauth2/token'
AutParams = {
    'client_id': os.environ.get("TWITCH_CLIENT_ID"),
    'client_secret': os.environ.get("TWITCH_CLIENT_SECRET"),
    'grant_type': 'client_credentials'
}


def connect_to_twitch_endpoint(endpoint, params=None):

    url = f"https://api.twitch.tv/helix/{endpoint}"
    AutCall = requests.post(url=authURL, params=AutParams)
    access_token = AutCall.json()['access_token']

    head = {
        'Client-ID': AutParams.get('client_id'),
        'Authorization':  "Bearer " + access_token,
    }

    response = requests.get(url, headers=head, params=params)

    if response.status_code != 200:
        raise Exception(
            "Request to url {} returned an error: {} {}".format(
                response.url, response.status_code, response.text
            )
        )

    return response.json()

