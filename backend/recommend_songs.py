from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API認証
client_id = '20e9a4be685749e2bf74fa422a90ee77'
client_secret = 'c2ebbce0ad1d4b43b086e377fa1368f5'

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

key_pitch_map = {
    0: 261.63, 1: 277.18, 2: 293.66, 3: 311.13, 4: 329.63,
    5: 349.23, 6: 369.99, 7: 392.00, 8: 415.30, 9: 440.00,
    10: 466.16, 11: 493.88
}

def pitch_in_range(track_key, track_mode, user_lowest_pitch, user_highest_pitch):
    base_pitch = key_pitch_map[track_key]
    if track_mode == 0:  # マイナーキーの場合
        base_pitch *= 0.9
        if user_highest_pitch < 200:
            return base_pitch >= user_lowest_pitch
    return user_lowest_pitch <= base_pitch <= user_highest_pitch

def get_recommended_songs(user_lowest_pitch=key_pitch_map[0], user_highest_pitch=key_pitch_map[11], limit=30):
    recommended_tracks = []
    offset = 0
    max_try=100
    n=0
    if(user_highest_pitch<key_pitch_map[0] or user_lowest_pitch>key_pitch_map[11]):return []
    while len(recommended_tracks) < limit and n<max_try:
        results = sp.search(q='year:2020-2023', type='track', limit=50, offset=offset, market='JP')
        if not results['tracks']['items']:
            break

        track_ids = [track['id'] for track in results['tracks']['items']]
        features_list = sp.audio_features(track_ids)

        for i, track in enumerate(results['tracks']['items']):
            if len(recommended_tracks) >= limit:
                break

            features = features_list[i]
            if features and pitch_in_range(features['key'], features['mode'], user_lowest_pitch, user_highest_pitch):
                recommended_tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                })
        n+=1
        offset += 100

    return recommended_tracks
