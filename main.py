import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import os

client_id = os.environ["CLIENT-ID"]
client_secret = os.environ["CLIENT-SECRET"]
user_uri = os.environ["USER-URI"]
username = os.environ["USER-NAME"]



time_travel =  input("Which year do you want to relive?? Type data in this format YYYY-MM-DD:\n")



URL = f"https://www.billboard.com/charts/hot-100/{time_travel}/"

respsonse = requests.get(URL)
data = respsonse.text
# print(data)

classs = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"

soup = BeautifulSoup(data, features="html.parser")

song_name = soup.find_all("div", class_="o-chart-results-list-row-container")

# print(song_name)
song_list = []

for w in song_name:
    song = (((w.find("ul")).find("h3")).text)
    translator = str.maketrans({chr(10): '', chr(9): ''})
    song_transtalted = song.translate(translator)
    song_list.append(song_transtalted)
    # print(song_transtalted)




dated = time_travel.split(sep="-")



# SPOTIFY AUTH

scope = "playlist-modify-private"
#
ssp = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=user_uri, scope=scope, cache_path="token.txt", username=username, show_dialog=True)

sp = spotipy.Spotify(auth_manager=ssp)

user_id = sp.current_user()["id"]

song_list_uri = []

for g in song_list:
    try:
        query = {
            "track": f"{g}",
            "year": f"{dated[0]}"
        }
        qq = str(query)
        x = sp.search(q=qq, type="track")
        gg = x["tracks"]["items"][0]["uri"]
        song_list_uri.append(gg)
    except:
        IndexError


new_playlist =  sp.user_playlist_create(user=user_id, name=f"{time_travel} BILLBOARD PLAY LIST", public=False, description=f"Top tracks from {time_travel} ")
sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist["id"], tracks=song_list_uri)