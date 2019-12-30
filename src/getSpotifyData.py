# shows a user's playlists (need to be authenticated via oauth)

import spotipy
import spotipy.util as util
import time


def spotify_login():
    username = ""
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope, client_id='',
                                           client_secret='',
                                           redirect_uri='http://localhost/')
    if token:
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        print("Can't get token for", username)


def get_liked_songs():
    sp = spotify_login()
    offset_amount = 0
    difference = 0
    song_step = 50
    playlists = sp.current_user_saved_tracks(limit=1)
    total_songs = playlists["total"]
    difference = total_songs
    songlist = []
    while offset_amount < total_songs:
        if difference <= song_step:
            print("last song amout : " + str(difference))
            songlist = songlist + sp.current_user_saved_tracks(offset=offset_amount, limit=difference)["items"]
            offset_amount = total_songs
            return songlist

        songlist = songlist + sp.current_user_saved_tracks(offset=offset_amount,limit=song_step)["items"]
        offset_amount = offset_amount + song_step
        difference = total_songs - offset_amount
        time.sleep(0.2)
        print("got " + str(offset_amount) + " out of " + str(total_songs) + " liked songs")
    return songlist

