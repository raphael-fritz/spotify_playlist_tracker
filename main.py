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
#   - implement change tracking for removals
#       -> implement + and - as indicators for addition/removal
#   - apply all tracking for playlists to song in playlists
#   - cleanup
#   - more cleanup


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
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
        playlist_file.readline()  # discard timestamp
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


def create_dir_structure(username, playlists):

    # check if user directory exists and create if not
    if not Path(username).is_dir():
        print(username + "'s directory doesn't exist and will be created")
        Path(username).mkdir()

    # check if playlists file exists and create if not
    pl_str = username + "/playlists.txt"
    if not Path(pl_str).is_file():
        print(pl_str + " doesn't exist and will be created")
        Path(pl_str).touch()

    # check if playlists_changes file exists and create if not
    pl_str = username + "/playlists_changes.txt"
    if not Path(pl_str).is_file():
        print(pl_str + " doesn't exist and will be created")
        Path(pl_str).touch()

    # check if playlist directories exists and create if not
    for i in range(playlists.__len__()):
        pl_path_str = username + "/" + playlists[i]
        songs_str = pl_path_str + "/" + playlists[i] + "_songs.txt"
        songs_changes_str = pl_path_str + "/" + \
            playlists[i] + "_songs_changes.txt"

        if not Path(pl_path_str).is_dir():
            print(pl_path_str + " doesn't exist and will be created")
            Path(pl_path_str).mkdir()

        if not Path(songs_str).is_file():
            print(songs_str + " doesn't exist and will be created")
            Path(songs_str).touch()

        if not Path(songs_changes_str).is_file():
            print(songs_changes_str + " doesn't exist and will be created")
            Path(songs_changes_str).touch()


if __name__ == '__main__':

    time_str = str(datetime.datetime.fromtimestamp(time.time()))
    print(time_str, "\n")

    # authenticate with spotify
    scope = "playlist-modify-public"
    spotify = spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope=scope)

    usernames = get_usernames()
    pl_names = []
    user_list = []

    # create/update directory structure
    for username in usernames:
        user = Spotify_User(spotify, username['name'], username['id'])
        user_list.append(user)
        for pl in user.playlists:
            pl_names.append(pl['name'])
        create_dir_structure(user.name, pl_names)

    # compare/update playlist/song files
    for user in user_list:
        pl_file_str = user.name + "/playlists.txt"
        pl_changes_file_str = user.name + "/playlists_changes.txt"
        pl_baseline = []
        pl_current = []

        # read playlist file
        with open(pl_file_str, "r", encoding="utf-8") as pl_file:
            for line in pl_file.readlines():
                pl_baseline.append(line.strip("\n"))
        pl_current = pl_names

        print(pl_baseline)
        print(pl_current)

        # get changes
        diff = list(set(set(pl_current)-set(pl_baseline))) # currently only works for additions 
        print(diff)

        # write playlist file
        with open(pl_file_str, "w", encoding="utf-8") as pl_file:
            for pl in pl_names:
                pl_file.write(str(pl+"\n"))

        # write playlist changes file
        with open(pl_changes_file_str, "a", encoding="utf-8") as diff_file:
            diff_file.write(str("\n" + str(datetime.datetime.fromtimestamp(time.time())) + "\n"))
            for change in diff:
                diff_file.write(str(change+"\n"))

    # get all tracks from a playlist
    print("\n")
    pl_uri = "maflra:playlist:6K91vRPSfuUUIvd8xc82Hp"
    pl = Spotify_Playlist(spotify, pl_uri)
    tracks = pl.tracks
    for track in tracks:
        print(track['name'], "-", track['artists'][0]['name'])
