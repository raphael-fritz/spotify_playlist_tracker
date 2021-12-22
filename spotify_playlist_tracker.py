import spotipy
from spotify_user import Spotify_Playlist, Spotify_User
from pathlib import Path
from datetime import datetime


def spotify_authentication(client_id:str, client_secrect:str, redirect_uri:str, scope:str, openBrowser:bool) -> spotipy.client.Spotify:
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id=client_id, client_secret=client_secrect, redirect_uri=redirect_uri, scope=scope, open_browser=openBrowser)
    return spotipy.client.Spotify(auth_manager=auth_manager)


def get_spotify_users(spotify: spotipy.client.Spotify) -> "list[Spotify_User]":
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
        print("\n\t" + user.name + ": Success!", end="")
        user_list.append(user)
    return user_list


def get_tracks(spotify: spotipy.client.Spotify, uri: str) -> "list[str]":
    tracks = []
    for track in Spotify_Playlist(spotify, uri).tracks:
        tracks.append(str(track["artists"][0]["name"] + "-" + track["name"]))
    return tracks


def get_diff(list1: list, list2: list) -> tuple:
    diff_p = list(set(set(list1)-set(list2)))
    diff_n = list(set(set(list2)-set(list1)))
    return (diff_p, diff_n)


def check_dir(path: str) -> None:
    if not Path(path).is_dir():
        print(path + " doesn't exist and will be created")
        Path(path).mkdir()


def check_file(path: str) -> None:
    if not Path(path).is_file():
        print(path + " doesn't exist and will be created")
        Path(path).touch()


def create_dir_structure(user_list:"list[Spotify_User]") -> None:
    check_dir("data")
    for user in user_list:
        check_dir(user.user_path)
        check_file(user.pl_path)
        check_file(user.pl_changes_path)
        for path in user.song_path_list:
            check_file(path)
        for path in user.song_changes_path_list:
            check_file(path)


def read_base_file(path: str) -> "list[str]":
    with open(path, "r", encoding="utf-8") as file:
        lines = []
        for line in file.readlines():
            lines.append(line.strip("\n"))
        return lines


def write_base_file(path: str, base_list: list) -> None:
    with open(path, "w", encoding="utf-8") as file:
        for entry in base_list:
            file.write(str(entry + "\n"))


def write_diff_file(path: str, header: str, diff_list: "tuple[list, list]") -> None:
    with open(path, "a", encoding="utf-8") as file:
        (diff_p, diff_n) = diff_list
        print(header + ":", end="")
        if diff_p or diff_n:
            file.write(
                str("\n" + str(datetime.now()) + "\n"))
            for change in diff_p:
                diff_str = str("+ " + change + "\n")
                file.write(diff_str), print(diff_str, end="")
            for change in diff_n:
                diff_str = str("- " + change + "\n")
                file.write(diff_str), print(diff_str, end="")
        else:
            print(" x no changes")


def update_dir_structure(spotify:spotipy.client.Spotify, user_list: "list[Spotify_User]") -> None:
    for user in user_list:
        pl_current = user.playlist_names
        pl_baseline = read_base_file(user.pl_path)

        (diff_p, diff_n) = get_diff(pl_current, pl_baseline)
            

        write_base_file(user.pl_path, pl_current)
        write_diff_file(user.pl_changes_path, str("\t" + user.name), (diff_p, diff_n))

        for i in range(len(user.playlists)):
            #try:
            tracks_current = user.playlists[i].track_names
            tracks_baseline = read_base_file(user.song_path_list[i])
            (diff_p, diff_n) = get_diff(tracks_current, tracks_baseline)

            write_base_file(user.song_path_list[i], tracks_current)
            write_diff_file(user.song_changes_path_list[i], str("\t\t"+
                user.name + ": " + user.playlists[i].name), (diff_p, diff_n))
                #i += 1
            """except ValueError:
                print("\t\t" + user.name + ": " + user.playlists[i].name + ": ValueError")
                i += 1
                pass"""
