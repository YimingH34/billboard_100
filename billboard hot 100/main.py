import bs4
import requests
import re
import pandas
import spotipy
import os

year = input('What year do you want to travel to? Type the date in this format YYYY-MM-DD')
link = f'https://www.billboard.com/charts/hot-100/{year}'
date = year.split('-')
uwu = date[0]
print(uwu)
response = requests.get(link)
soup = bs4.BeautifulSoup(response.text, 'html.parser')
g = soup.findAll('li')
song_list = []
for song in g:
    h = (song.find(class_='c-title', id="title-of-a-story"))
    try:
        song_list.append(h.getText())
    except:
        pass
list = []
for i in range(len(song_list)):
    v = re.sub('\s+', '', song_list[i])
    list.append(v)
list = pandas.Series(list).unique().tolist()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
        show_dialog=True,
        cache_path="token.txt",
        username='Yiming Huang',
    )
)
user_id = sp.current_user()["id"]

s_uri = []
for song in song_list:
    result = sp.search(q=f'track:{song} year:{uwu}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        s_uri.append(uri)
    except:
        print(f'{song} not on spotify')

v = sp.user_playlist_create(user=user_id, name=f'{year} Billboard 100', public=False,
                            description=f'The top 100 musics for {year}')
s_uri = pandas.Series(s_uri).unique().tolist()
sp.playlist_add_items(playlist_id=v['id'], items=s_uri)
print('success')
