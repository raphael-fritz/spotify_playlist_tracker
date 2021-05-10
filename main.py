# spotify tracker
#
# to do:
#   - writing out changes in playlists
#   - apply all tracking for playlists to song in playlists
#   - cleanup
#   - more cleanup


import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import time
import datetime


def spotify_authentication(client_id, client_secrect, redirect_uri, scope):
    auth_manager = SpotifyOAuth(
        client_id=client_id, client_secret=client_secrect, redirect_uri=redirect_uri, scope=scope)
    return spotipy.Spotify(auth_manager=auth_manager)


def get_usernames():
    usernames = {}
    with open("usernames.txt") as f:
        for username in f:
            (name, id) = username.split()
            usernames[name] = id
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
            "status from "+str(datetime.datetime.fromtimestamp(time.time()))+"\n")
        for name in usernames:
            playlist_file.write((name + "'s Playlists:\n"))
            try:
                playlists = spotify.user_playlists(usernames[name])
                for playlist in playlists['items']:
                    playlist_file.write("\t"+playlist['name']+"\n")
                playlist_file.write("\n")
            except(spotipy.exceptions.SpotifyException):
                pass


def get_current_playlists(spotify, usernames):
    current = []
    for name in usernames:
        current.append((name + "'s Playlists:\n"))
        try:
            playlists = spotify.user_playlists(usernames[name])
            for playlist in playlists['items']:
                current.append("\t"+playlist['name']+"\n")
            current.append("\n")
        except(spotipy.exceptions.SpotifyException):
            pass
    return current


def get_playlist_changes(baseline, current):
    if baseline == current:
        return None
    else:
        diff = list(set(set(current)-set(baseline)))
        diff = str(diff).replace("['\\t", "").replace("\\n']", "")
        return diff


if __name__ == '__main__':

    time_str = str(datetime.datetime.fromtimestamp(time.time()))
    print(time_str)
    print(str(datetime.datetime.fromisoformat(time_str))+"\n")

    # authenticate with spotify
    scope = "playlist-modify-public"
    spotify = spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope=scope)

    usernames = get_usernames()
    baseline = get_playlist_baseline()
    current = get_current_playlists(spotify, usernames)
    diff = get_playlist_changes(baseline, current)

    for i in range(len(current)):
        if str(current[i]).find(diff) == 1:
            print(str(i)+str(current[i]))

    # get all tracks from a playlist
    pl_id = "maflra:playlist:43LYgPshFoeyjRhENW70e3"
    offset = 0
    while True:
        response = spotify.playlist_items(pl_id,
                                          offset=offset,
                                          fields='items.track.id,total',
                                          additional_types=['track'])

        if len(response['items']) == 0:
            break

        print(response['items'])
        offset = offset + len(response['items'])
        print(offset, "/", response['total'])

    print(response['items'])
