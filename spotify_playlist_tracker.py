import time
import datetime
import spotipy
import re
from pathlib import Path
from spotipy import SpotifyException
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotify_user import Spotify_Playlist, Spotify_User


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
        user = Spotify_User(spotify, username["name"], username["id"])
        user_list.append(user)
    return user_list


def get_playlists(user: Spotify_User):
    playlists = []
    for pl in user.playlists:
        playlists.append(pl["name"])
    return playlists


def get_tracks(spotify: Spotify, uri: str):
    try:
        tracks = []
        for track in Spotify_Playlist(spotify, uri).tracks:
            tracks.append(
                str(track["artists"][0]["name"] + "-" + track["name"]))
        return tracks
    except SpotifyException:
        pass


def rpl_bad_chars(string: str):
    bad_chars = {"ä": "ae", "ö": "oe", "ü": "ue",
                 "Ä": "AE", "Ö": "OE", "Ü": "UE", "ß": "ss", ".": "_"}
    rpl_pattern = r"(\s)|([^\w\-_\.\ ])"

    for char in bad_chars:
        string = string.replace(char, bad_chars[char])
    return re.sub(rpl_pattern, "_", string)


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


def check_dir(path: str):
    if not Path(path).is_dir():
        print(path + " doesn't exist and will be created")
        Path(path).mkdir()


def check_file(path: str):
    if not Path(path).is_file():
        print(path + " doesn't exist and will be created")
        Path(path).touch()


def create_dir_structure(user_list):
    for user in user_list:
        usr_str, pl_str, pl_changes_str, pl_path_list, songs_list, songs_changes_list = get_path_strings(
            user.name, get_playlists(user))

        check_dir(usr_str)
        check_file(pl_str)
        check_file(pl_changes_str)

        for i in range(pl_path_list.__len__()):
            check_dir(pl_path_list[i])
            check_file(songs_list[i])
            check_file(songs_changes_list[i])


def read_base_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        lines = []
        for line in file.readlines():
            lines.append(line.strip("\n"))
        return lines


def write_base_file(path: str, base_list: list):
    with open(path, "w", encoding="utf-8") as file:
        for entry in base_list:
            file.write(str(entry + "\n"))


def write_diff_file(path: str, header: str, diff: "tuple[list, list]"):
    with open(path, "a", encoding="utf-8") as file:
        print("\n" + header + ":")
        (diff_p, diff_n) = diff
        if diff_p or diff_n:
            file.write(
                str("\n" + str(datetime.datetime.fromtimestamp(time.time())) + "\n"))
            for change in diff_p:
                diff_str = str("+ " + change + "\n")
                file.write(diff_str), print(diff_str, end="")
            for change in diff_n:
                diff_str = str("- " + change + "\n")
                file.write(diff_str), print(diff_str, end="")
        else:
            print("x no changes")


def update_dir_structure(spotify, user_list: "list[Spotify_User]"):
    for user in user_list:
        pl_current = get_playlists(user)
        pl_str, pl_changes_str = get_path_strings(
            user.name, pl_current)[1:3]
        pl_baseline = read_base_file(pl_str)
        (diff_p, diff_n) = get_diff(pl_current, pl_baseline)

        write_base_file(pl_str, pl_current)
        write_diff_file(pl_changes_str, user.name, (diff_p, diff_n))

        i = 0
        songs_list, songs_changes_list = get_path_strings(
            user.name, get_playlists(user))[4:6]
        for playlist in user.playlists:
            try:
                tracks_current = get_tracks(spotify, playlist["uri"])
                tracks_baseline = read_base_file(songs_list[i])
                (diff_p, diff_n) = get_diff(tracks_current, tracks_baseline)

                write_base_file(songs_list[i], tracks_current)
                write_diff_file(songs_changes_list[i], str(
                    user.name + ": " + playlist["name"]), (diff_p, diff_n))
                i += 1

            except TypeError:
                pass
