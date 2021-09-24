import time
import datetime
import spotipy
import re
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from spotify_user import Spotify_User


def rpl_bad_chars(str: str):
    bad_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
                 'Ä': 'AE', 'Ö': 'OE', 'Ü': 'UE', 'ß': 'ss', '.': '_'}
    rpl_pattern = r"(\s)|([^\w\-_\.\ ])"

    for char in bad_chars:
        str = str.replace(char, bad_chars[char])
    return re.sub(rpl_pattern, '_', str)


def spotify_authentication(client_id, client_secrect, redirect_uri, scope):
    auth_manager = SpotifyOAuth(
        client_id=client_id, client_secret=client_secrect, redirect_uri=redirect_uri, scope=scope)
    return spotipy.Spotify(auth_manager=auth_manager)


def get_spotify_users(spotify):
    usernames = []
    with open("usernames.txt") as f:
        for username in f:
            (name, id) = username.split()
            user = {
                "name": name,
                "id": id
            }
            usernames.append(user)

    user_list = []
    for username in usernames:
        user = Spotify_User(spotify, username['name'], username['id'])
        user_list.append(user)
    return user_list


def create_dir_structure(user_list):
    for user in user_list:
        usr_str = rpl_bad_chars(user.name)

        # check if user directory exists and create if not
        if not Path(usr_str).is_dir():
            print(usr_str + "'s directory doesn't exist and will be created")
            Path(usr_str).mkdir()

        # check if playlists file exists and create if not
        pl_str = usr_str + "/playlists.txt"
        if not Path(pl_str).is_file():
            print(pl_str + " doesn't exist and will be created")
            Path(pl_str).touch()

        # check if playlists_changes file exists and create if not
        pl_str = usr_str + "/playlists_changes.txt"
        if not Path(pl_str).is_file():
            print(pl_str + " doesn't exist and will be created")
            Path(pl_str).touch()

        # get playlists
        playlists = []
        for pl in user.playlists:
            playlists.append(pl['name'])

        # check if playlist directories exists and create if not
        for i in range(playlists.__len__()):
            playlist = rpl_bad_chars(playlists[i])
            pl_path_str = usr_str + "/" + playlist
            songs_str = pl_path_str + "/" + playlist + "_songs.txt"
            songs_changes_str = pl_path_str + "/" + playlist + "_songs_changes.txt"

            if not Path(pl_path_str).is_dir():
                print(pl_path_str + " doesn't exist and will be created")
                Path(pl_path_str).mkdir()

            if not Path(songs_str).is_file():
                print(songs_str + " doesn't exist and will be created")
                Path(songs_str).touch()

            if not Path(songs_changes_str).is_file():
                print(songs_changes_str + " doesn't exist and will be created")
                Path(songs_changes_str).touch()


def update_dir_structure(user_list):
    for user in user_list:
        usr_str = rpl_bad_chars(user.name)
        pl_file_str = usr_str + "/playlists.txt"
        pl_changes_file_str = usr_str + "/playlists_changes.txt"
        pl_baseline = []
        pl_current = []

        for pl in user.playlists:
            pl_current.append(pl['name'])

        # read playlist file
        with open(pl_file_str, "r", encoding="utf-8") as pl_file:
            for line in pl_file.readlines():
                pl_baseline.append(line.strip("\n"))

        # get changes
        diff1 = list(set(set(pl_current)-set(pl_baseline)))
        diff2 = list(set(set(pl_baseline)-set(pl_current)))

        # write playlist file
        with open(pl_file_str, "w", encoding="utf-8") as pl_file:
            for pl in pl_current:
                pl_file.write(str(pl+"\n"))

        # write playlist changes file
        with open(pl_changes_file_str, "a", encoding="utf-8") as diff_file:
            if diff1 or diff2:
                print("\n" + user.name + ":")
                diff_file.write(
                    str("\n" + str(datetime.datetime.fromtimestamp(time.time())) + "\n"))
                for change in diff1:
                    diff_str = str("+ " + change + "\n")
                    diff_file.write(diff_str), print(diff_str, end="")
                for change in diff2:
                    diff_str = str("- " + change + "\n")
                    diff_file.write(diff_str), print(diff_str, end="")


"""def get_playlist_baseline():
    # load playlist baseline
    baseline = []
    with open("user_playlists.txt", "r", encoding="utf-8") as playlist_file:
        playlist_file.readline()  # discard timestamp
        baseline = playlist_file.readlines()
    return baseline"""


"""def put_playlist_baseline(spotify, usernames):
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
                pass"""


"""def get_playlist_changes(baseline, current):
    if baseline == current:
        return None
    else:
        diff = list(set(set(current)-set(baseline)))
        diff = str(diff).replace("['\\t", "").replace("\\n']", "")
        return diff"""
