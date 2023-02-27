import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


# Expects a list of Song objects that have an artist and a track attribute
def update_playlist(songs):

    load_dotenv()

    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    user_id = sp.current_user()['id']


    playlist_name = "Netflix: Recently Heard"


    # Get all user playlists
    playlists = sp.user_playlists(user_id)
    found = False


    # Look for the designated playlist and get its id
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            found = True
        else:
            pass

    # Create the playlist ourselves if it isn't found, grab its id
    if not found:
        playlist = sp.user_playlist_create(user_id, playlist_name)
        playlist_id = playlist['id']


    song_ids = []

    for song in songs:
        results = sp.search(q='artist:' + song.artist + ' track:' + song.track, type='track', limit=25)
        items = results['tracks']['items']
        if len(items) > 0:
            song_id = items[0]['id']
        else:
            pass

        song_ids.append(song_id)


    sp.playlist_replace_items(playlist_id, song_ids)

