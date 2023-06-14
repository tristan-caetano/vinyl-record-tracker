# Tristan Caetano
# Spotify API Accesser
# Accessing the spotify API and grabbing associated info

# Importing
import pandas as pd
import requests
import request_tester as rt

# Getting required api info
def access_spotify():

    # Getting api key (not included in repo)
    keys = pd.read_csv('spotify_api_info.csv')
    apikey = keys['clientid'][0]

    # Making sure access is granted
    auth_url = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': keys['clientid'][0],
    'client_secret': keys['clientsecret'][0],
    })

    return auth_response.json()


# Main API interfacer
def get_album_info():

    # Getting access token
    authentication = access_spotify()
    access_token = authentication['access_token']

    # Setting token for header
    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # Setting up url
    #url = "https://api.spotify.com/v1/"
    url = 'https://api.spotify.com/v1/'
    # 'https://api.spotify.com/v1/search?q=To+Pimp+a+Butterfly&type=album'
    # Album ID (TPAB)
    q = "To+Pimp+a+Butterfly"
    type = "album"

    # Getting request
    r = requests.get(url + 'search?q=' + q + "&type=" + type, headers=headers)
    info = r.json()
    print(info['albums']['items'][0]['name'])
    print(info['albums']['items'][0]['artists'][0]['name'])

    # # Extracting all needed info
    # print(r.json())

get_album_info()