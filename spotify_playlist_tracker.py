import json
import spotipy
from spotify_user import Spotify_Playlist, Spotify_User
from pathlib import Path
from datetime import date, datetime, time

PATH = "events.txt"
ENC = "utf-8"


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


def check_log(path: str) -> None:
    if not Path(path).is_file():
        Path(path).touch()
    global PATH
    PATH = path


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


def cmp_tracks(item1, item2: "dict[str, str, str, list]",):
    for (key1, key2) in zip(item1.keys(), item2.keys()):
        if (item1[key1] == item2[key2]) and not key1 == key2 == "data":
            print(key1, item1[key1], key2, item2[key2])
        elif key1 == key2 == "data":
            print(type(item1[key1]), type(item2[key2]))
            if type(item1[key1]) == type(item2[key2]) == list:
                for (entry1, entry2) in zip(item1[key1], item2[key2]):
                    if type(entry1) == type(entry2) == dict:
                        cmp_tracks(entry1, entry2)
                    elif type(entry1) == type(entry2) == str:
                        diff_p = set(entry1)-set(entry2)
                        diff_n = set(entry2)-set(entry1)
                        print(diff_p, diff_n)

        else:
            print(key1, key2)
            print("hello")


def get_diff(list1: list, list2: list) -> tuple:
    diff_p = list(set(set(list1)-set(list2)))
    diff_n = list(set(set(list2)-set(list1)))
    return (diff_p, diff_n)


"""def cmp_tracks(item1:"dict[str, str, str, list[dict[str, str, str, list[str]]]]", item2):
    for (key1, key2) in zip(item1.keys(), item2.keys()):
        if (item1[key1] != item2[key2]) and not key1==key2=="data":
            print("cannot compare")
        elif key1==key2=="data":
            for entry1, entry2 in zip(item1[key1], item2[key2]):
                print(entry1.keys())"""


def update_pl(playlist: Spotify_Playlist):
    items = []
    for track in playlist.tracks:
        time = datetime.strptime(track.added_at, "%Y-%m-%dT%H:%M:%SZ")
        item = {
            "timestamp": str(time),
            "op": "+",
            "type": "track",
            "data": [
                {
                    "name": track.artist_and_name,
                    "id": track.id
                }
            ]
        }
        items.append(item)

    data = {
        "id": playlist.id,
        "type": "playlist",
        "op": "+-",
        "data": items
    }
    return data


def update_user(user: Spotify_User):
    items = []
    for playlist in user.playlists:
        items.append(update_pl(playlist))

    data = {
        "id": str(user.id),
        "type": "user",
        "op": "+-",
        "data": items
    }

    with open("log.txt", "w+") as file:
        file.write(json.dumps(data, indent=4))
    with open(PATH, "a+", encoding=ENC) as file:
        file.write(str(json.dumps(data)+"\n"))
    return data


def read_user_events(user: Spotify_User):
    with open(PATH, "r", encoding=ENC) as file:
        events = []
        for line in file.readlines():
            item = json.loads(line)
            res = search_item(item, "maflra", "user")
            if res != None:
                events.append(res)
            res = search_item(item, "6K91vRPSfuUUIvd8xc82Hp", "playlist")
            if res != None:
                events.append(res)
            res = search_item(item, "3JKfyBJZvr3hENnSokG7RQ", "track")
            if res != None:
                events.append(res)
            break
        return events


def search_item(item: "dict[str, str, str, list]", id_, type_):
    if type_ == "playlist" or type_ == "user":
        try:
            if item["id"] == id_ and item["type"] == type_:
                return item
            elif type(item["data"]) == list:
                items = []
                for entry in item["data"]:
                    if type(entry) == dict:
                        it = search_item(entry, id_, type_)
                        if it != None:
                            items.append(it)
                if items != []:
                    return {
                        "id": item["id"],
                        "type": item["type"],
                        "op": item["op"],
                        "data": [
                            {
                                "id": entry["id"],
                                "op":entry["op"],
                                "type":entry["type"],
                                "data":items
                            }
                        ]
                    }

                else:
                    return None
            else:
                return None
        except KeyError:
            return None
    elif type_ == "track":
        if type(item) == dict:
            for entry in item["data"]:
                if entry["id"] == id_ and item["type"] == type_:
                    return entry
                try:
                    if type(entry["data"]) == list:
                        items = []
                        for line in entry["data"]:
                            if type(line) == dict:
                                it = search_item(line, id_, type_)
                                if it != None:
                                    items.append(it)
                        if items != []:
                            return {
                                "id": item["id"],
                                "type": item["type"],
                                "op": item["op"],
                                "data": [
                                    {
                                        "id": entry["id"],
                                        "op":entry["op"],
                                        "type":entry["type"],
                                        "data":[
                                            {
                                                "type": str(type_),
                                                "timestamp": line["timestamp"],
                                                "op":line["op"],
                                                "data":items
                                            }
                                        ]
                                    }
                                ]
                            }
                    else:
                        return None
                except KeyError:
                    return None
                else:
                    return None
            return None
