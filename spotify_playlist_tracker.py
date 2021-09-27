import time
import datetime
import spotipy
import re
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from spotify_user import Spotify_User


def rpl_bad_chars(string: str):
    bad_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
                 'Ä': 'AE', 'Ö': 'OE', 'Ü': 'UE', 'ß': 'ss', '.': '_'}
    rpl_pattern = r"(\s)|([^\w\-_\.\ ])"

    for char in bad_chars:
        string = string.replace(char, bad_chars[char])
    return re.sub(rpl_pattern, '_', string)


def spotify_authentication(client_id, client_secrect, redirect_uri, scope):
    auth_manager = SpotifyOAuth(
        client_id=client_id, client_secret=client_secrect, redirect_uri=redirect_uri, scope=scope)
    return spotipy.Spotify(auth_manager=auth_manager)


def get_spotify_users(spotify: Spotify):
    usernames = []
    with open("usernames.txt") as username_list:
        for username in username_list:
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


def get_playlists(user: Spotify_User):
    playlists = []
    for pl in user.playlists:
        playlists.append(pl['name'])
    return playlists


def get_path_strings(username: str, playlists: list):
    usr_str = rpl_bad_chars(username)
    pl_str = usr_str + "/playlists.txt"
    pl_changes_str = usr_str + "/playlists_changes.txt"
    pl_path_list = []
    songs_list = []
    songs_changes_list = []

    for playlist in playlists:
        playlist = rpl_bad_chars(playlist)
        pl_path_list.append(str(usr_str + "/" + playlist))
        songs_list.append(str(usr_str + "/" + playlist +
                              "/" + playlist + "_songs.txt"))
        songs_changes_list.append(
            str(usr_str + "/" + playlist + "/" + playlist + "_songs_changes.txt"))

    return usr_str, pl_str, pl_changes_str, pl_path_list, songs_list, songs_changes_list


def get_diff(list1: list, list2: list):
    diff_p = list(set(set(list1)-set(list2)))
    diff_n = list(set(set(list2)-set(list1)))
    return (diff_p, diff_n)


def create_dir_structure(user_list):
    for user in user_list:
        usr_str, pl_str, pl_changes_str, pl_path_list, songs_list, songs_changes_list = get_path_strings(
            user.name, get_playlists(user))

        # check if user directory exists and create if not
        if not Path(usr_str).is_dir():
            print(usr_str + "'s directory doesn't exist and will be created")
            Path(usr_str).mkdir()

        # check if playlists file exists and create if not
        if not Path(pl_str).is_file():
            print(pl_str + " doesn't exist and will be created")
            Path(pl_str).touch()

        # check if playlists_changes file exists and create if not
        if not Path(pl_changes_str).is_file():
            print(pl_changes_str + " doesn't exist and will be created")
            Path(pl_changes_str).touch()

        # check if playlist directories exists and create if not
        for i in range(pl_path_list.__len__()):

            if not Path(pl_path_list[i]).is_dir():
                print(pl_path_list[i] + " doesn't exist and will be created")
                Path(pl_path_list[i]).mkdir()

            if not Path(songs_list[i]).is_file():
                print(songs_list[i] + " doesn't exist and will be created")
                Path(songs_list[i]).touch()

            if not Path(songs_changes_list[i]).is_file():
                print(songs_changes_list[i] +
                      " doesn't exist and will be created")
                Path(songs_changes_list[i]).touch()


def update_dir_structure(user_list):
    for user in user_list:
        pl_str, pl_changes_str = get_path_strings(
            user.name, get_playlists(user))[1:3]
        pl_current = get_playlists(user)
        pl_baseline = []

        # read playlist file
        with open(pl_str, "r", encoding="utf-8") as pl_file:
            for line in pl_file.readlines():
                pl_baseline.append(line.strip("\n"))

        # write playlist file
        with open(pl_str, "w", encoding="utf-8") as pl_file:
            for pl in pl_current:
                pl_file.write(str(pl+"\n"))

        # write playlist changes file
        with open(pl_changes_str, "a", encoding="utf-8") as diff_file:
            (diff_p, diff_n) = get_diff(pl_current, pl_baseline)
            if diff_p or diff_n:
                print("\n" + user.name + ":")
                diff_file.write(
                    str("\n" + str(datetime.datetime.fromtimestamp(time.time())) + "\n"))
                for change in diff_p:
                    diff_str = str("+ " + change + "\n")
                    diff_file.write(diff_str), print(diff_str, end="")
                for change in diff_n:
                    diff_str = str("- " + change + "\n")
                    diff_file.write(diff_str), print(diff_str, end="")
