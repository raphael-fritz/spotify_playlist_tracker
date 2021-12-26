from sys import prefix
import spotipy
from spotify_user import Spotify_Playlist, Spotify_User
from pathlib import Path
from datetime import datetime, timedelta


def spotify_authentication(client_id: str, client_secrect: str, redirect_uri: str, scope: str, openBrowser: bool) -> spotipy.client.Spotify:
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id=client_id, client_secret=client_secrect, redirect_uri=redirect_uri, scope=scope, open_browser=openBrowser)
    return spotipy.client.Spotify(auth_manager=auth_manager)


def get_spotify_user(spotify: spotipy.client.Spotify, username: "dict[str, str]") -> Spotify_User:
    user = Spotify_User(spotify, username["name"], username["id"])
    return user


def get_spotify_pl(spotify: spotipy.client.Spotify, pl_name: "dict[str, str]") -> Spotify_User:
    pl = Spotify_Playlist(spotify, pl_name["name"], pl_name["id"])
    return pl


def get_diff(list1: list, list2: list) -> tuple:
    diff_p = list(set(set(list1)-set(list2)))
    diff_n = list(set(set(list2)-set(list1)))
    return (diff_p, diff_n)


def check_dir(path: str) -> None:
    if not Path(path).is_dir():
        Path(path).mkdir()


def check_file(path: str) -> None:
    if not Path(path).is_file():
        Path(path).touch()


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


def write_diff_file(path: str, diff_list: "tuple[list, list]") -> None:
    (diff_p, diff_n) = diff_list
    if diff_p or diff_n:
        with open(path, "a", encoding="utf-8") as file:
            file.write(str("\n" + str(datetime.now()) + "\n"))
            for change in diff_p:
                diff_str = str("+ " + change + "\n")
                file.write(diff_str)
            for change in diff_n:
                diff_str = str("- " + change + "\n")
                file.write(diff_str)
    else:
        pass


def create_user_dir(user: Spotify_User) -> None:
    check_dir(user.user_path)
    check_file(user.pl_path)
    check_file(user.pl_changes_path)
    for i in range(len(user.playlists)):
        check_file(user.song_path_list[i])
        check_file(user.song_changes_path_list[i])


def update_user_dir(user: Spotify_User) -> None:
    pl_current = []
    for playlist in user.playlists:
        pl_current.append(playlist.name)
    pl_baseline = read_base_file(user.pl_path)
    (diff_p, diff_n) = get_diff(pl_current, pl_baseline)
    write_base_file(user.pl_path, pl_current)
    write_diff_file(user.pl_changes_path, (diff_p, diff_n))

    for i in range(len(user.playlists)):
        tracks_current = user.playlists[i].track_names
        tracks_baseline = read_base_file(user.song_path_list[i])
        (diff_p, diff_n) = get_diff(tracks_current, tracks_baseline)

        write_base_file(user.song_path_list[i], tracks_current)
        write_diff_file(user.song_changes_path_list[i], (diff_p, diff_n))


def get_usernames(path: str) -> "list[dict[str, str]]":
    usernames = []
    with open(path) as username_list:
        for username in username_list.readlines():
            (name, id) = username.split()
            user = {
                "name": name,
                "id": id
            }
            usernames.append(user)
    return usernames


def create_pl_dir(playlist: Spotify_Playlist) -> None:
    pl_path = "data/playlists/"
    check_dir(pl_path)
    check_file(str(pl_path + playlist.path))
    check_file(str(pl_path + playlist.changes_path))


def update_pl_dir(playlist: Spotify_Playlist) -> None:
    pl_path = "data/playlists/"
    tracks_current = playlist.track_names
    tracks_baseline = read_base_file(str(pl_path + playlist.path))
    (diff_p, diff_n) = get_diff(tracks_current, tracks_baseline)
    write_base_file(str(pl_path + playlist.path), tracks_current)
    write_diff_file(str(pl_path + playlist.changes_path), (diff_p, diff_n))


def get_playlists(path: str) -> "list[dict[str, str]]":
    playlists = []
    with open(path) as playlist_list:
        for playlist in playlist_list.readlines():
            (name, id) = playlist.split()
            playlist = {
                "name": name,
                "id": id
            }
            playlists.append(playlist)
    return playlists


def read_timestamps(lines: "list[str]") -> "list[dict[int, datetime]]":
    timestamps = []
    for idx, line in enumerate(lines):
        try:
            time = datetime.strptime(line.strip(), "%Y-%m-%d %H:%M:%S.%f")
            time_id = {
                "idx": idx,
                "time": time
            }
            timestamps.append(time_id)
        except ValueError:
            pass
    return timestamps


def read_chng(idx: int, lines: "list[str]", prefix="", suffix="\n",) -> str:
    j = idx+1
    chnge_string = str(prefix+lines[idx].strip()+suffix)
    while j < len(lines) and (lines[j][0] == "+" or lines[j][0] == "-"):
        chnge_string += str(prefix+lines[j].strip()+suffix)
        j += 1
    return chnge_string


def read_user_dir(user: Spotify_User, start_date=None, end_date=datetime.now()):
    summary = []
    with open(user.pl_changes_path, "r", encoding="utf-8") as file:
        changes = []
        lines = file.readlines()
        timestamps = read_timestamps(lines)
        if start_date == None:
            for time in timestamps:
                if time["time"] <= end_date:
                    changes.append(
                        read_chng(time["idx"], lines, prefix="\t\t"))
        else:
            for time in timestamps:
                if time["time"] <= end_date and time["time"] >= start_date:
                    changes.append(
                        read_chng(time["idx"], lines, prefix="\t\t"))
                        
        if not(changes==[]):
            summary.append(str("\t"+"playlists:"))
            for change in changes:
                summary.append(change)

    for i, path in enumerate(user.song_changes_path_list):
        with open(path, "r", encoding="utf-8") as file:
            changes = []
            lines = file.readlines()
            timestamps = read_timestamps(lines)
            if start_date == None:
                for time in timestamps:
                    if time["time"] <= end_date:
                        changes.append(
                            read_chng(time["idx"], lines, prefix="\t\t"))
            else:
                for time in timestamps:
                    if time["time"] <= end_date and time["time"] >= start_date:
                        change = read_chng(time["idx"], lines, prefix="\t\t")
                        changes.append(change)
            
            if not(changes==[]):
                summary.append(str("\t"+user.playlists[i].name+":"))
                for change in changes:
                    summary.append(change)
    return summary
