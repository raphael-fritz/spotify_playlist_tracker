# spotify tracker
#
# to do:
#   - writing out changes in playlists, output should look something like this:
#       time
#          user1:
#               + playlist 2
#               - playlist 1
#          user2:
#               ...
#
#   - apply all tracking for playlists to song in playlists
#   - cleanup
#   - more cleanup


import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import time
import datetime

from spotify_user import Spotify_User, Spotify_Playlist


def spotify_authentication(client_id, client_secrect, redirect_uri, scope):
    auth_manager = SpotifyOAuth(
        client_id=client_id, client_secret=client_secrect, redirect_uri=redirect_uri, scope=scope)
    return spotipy.Spotify(auth_manager=auth_manager)


def get_usernames():
    usernames = []
    with open("usernames.txt") as f:
        for username in f:
            (name, id) = username.split()
            user = {
                "name": name,
                "id": id
            }
            usernames.append(user)
    return usernames


def get_playlist_baseline():
    # load playlist baseline
    baseline = []
    with open("user_playlists.txt", "r", encoding="utf-8") as playlist_file:
        # discard timestamp
        playlist_file.readline()
        baseline = playlist_file.readlines()
    return baseline


def put_playlist_baseline(spotify, usernames):
    with open("user_playlists.txt", "w", encoding="utf-8") as playlist_file:
        playlist_file.write(
            str(datetime.datetime.fromtimestamp(time.time()))+":\n")
        for name in usernames:
            playlist_file.write((name + "'s Playlists:\n"))
            try:
                playlists = spotify.user_playlists(usernames[name])
                for playlist in playlists['items']:
                    playlist_file.write("\t"+playlist['name']+"\n")
                playlist_file.write("\n")
            except(spotipy.exceptions.SpotifyException):
                pass


def get_playlist_changes(baseline, current):
    if baseline == current:
        return None
    else:
        diff = list(set(set(current)-set(baseline)))
        diff = str(diff).replace("['\\t", "").replace("\\n']", "")
        return diff


if __name__ == '__main__':

    time_str = str(datetime.datetime.fromtimestamp(time.time()))
    print(time_str, "\n")
    # print(str(datetime.datetime.fromisoformat(time_str))+"\n")

    # authenticate with spotify
    scope = "playlist-modify-public"
    spotify = spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope=scope)

    usernames = get_usernames()

    # print user playlists
    users = []
    for username in usernames:
        user = Spotify_User(spotify, username['name'], username['id'])
        print(user.name, user.id)
        user_pl = user.playlists()
        for pl in user_pl:
            print(pl['name'])
        print("\n\n")

    # get all tracks from a playlist
    pl_uri = "maflra:playlist:4REFftIedZ7P0lXeAVtul6"
    pl = Spotify_Playlist(spotify, pl_uri)
    tracks = pl.tracks()
    for track in tracks:
        print(track['name'], "-", track['artists'][0]['name'])
