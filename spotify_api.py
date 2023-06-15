# Tristan Caetano
# Spotify API Accesser
# Accessing the spotify API and grabbing associated info

# Importing
import pandas as pd
import requests

# Getting required api info
def access_spotify():

    # Getting api key (not included in repo)
    keys = pd.read_csv('spotify_api_info.csv')

    # Making sure access is granted
    auth_url = 'https://accounts.spotify.com/api/token'

    # Getting authorization credentials
    auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': keys['clientid'][0],
    'client_secret': keys['clientsecret'][0],
    })

    # Returning authorization info
    return auth_response.json()

# Main API interfacer
def get_album_info(query):

    # Getting access token
    authentication = access_spotify()
    access_token = authentication['access_token']

    # Setting token for header
    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # Setting up url
    url = 'https://api.spotify.com/v1/'

    # Example of the search url string
    # 'https://api.spotify.com/v1/search?q=To+Pimp+a+Butterfly&type=album'

    # Item query
    type = "album"

    # Getting request
    r = requests.get(url + 'search?q=' + query + "&type=" + type, headers=headers)
    info = r.json()

    # Getting needed items
    album = info['albums']['items'][0]['name']
    artist = info['albums']['items'][0]['artists'][0]['name']
    num_of_tracks = info['albums']['items'][0]['total_tracks']
    release = info['albums']['items'][0]['release_date']
    cover = info['albums']['items'][0]['images'][0]['url']

    # Printing album info
    #print("Album:", album, "\nArtist:", artist, "\n# of Tracks:", num_of_tracks, "\nRelease Date:", release)

    # Returning Spotify album info
    return [album, artist, num_of_tracks, release, cover]