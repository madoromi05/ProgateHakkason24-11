import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify APIの認証
client_id = '20e9a4be685749e2bf74fa422a90ee77'
client_secret = 'c2ebbce0ad1d4b43b086e377fa1368f5'
#ユーザー認証が必要ない
#SpotifyClientCredentials秘密鍵

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# 曲の検索10曲くらい
results = sp.search(q='Imagine', type='track', limit=10)
for track in results['tracks']['items']:
    artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
    print(f"Track: {track['name']} by {artist_name}")

results = sp.search(q='中島みゆき', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx+1, track['name'])