from spotipy import SpotifyException
from re import sub


def rpl_bad_chars(string: str) -> str:
    bad_chars = {"ä": "ae", "ö": "oe", "ü": "ue",
                 "Ä": "AE", "Ö": "OE", "Ü": "UE", "ß": "ss", ".": "_"}

    for char in bad_chars:
        string = string.replace(char, bad_chars[char])
    return sub(r"(\s)|([^\w\-_\.\ ])", "_", string)


class Spotify_Playlist:

    def __init__(self, spotify, uri):
        self.spotify = spotify
        self.uri = uri
        self.tracks = self.get_tracks()
        if not len(self.tracks):
            raise ValueError


    def get_tracks(self):
        offset = 0
        tracks = []
        while True:
            response = self.spotify.playlist_items(self.uri,
                                                   offset=offset,
                                                   fields='items.track.id,total',
                                                   additional_types=['track'])

            if len(response['items']) == 0:
                break

            for item in response['items']:
                tracks.append(self.spotify.track(item['track']['id']))

            offset = offset + len(response['items'])
        return tracks


class Spotify_User:

    def __init__(self, spotify, user_name, user_id):
        self.spotify = spotify
        self.name = user_name
        self.id = user_id
        self.playlists = self.get_playlists()
        self.playlist_names = self.get_playlist_names()
        self.user_path = str("data/" + rpl_bad_chars(self.name))
        self.pl_path = str(self.user_path + "/_playlists.txt")
        self.pl_changes_path = str(self.user_path + "/_playlists_changes.txt")
        self.song_path_list, self.song_changes_path_list = self.get_song_paths()
        
    def get_song_paths(self) -> "tuple[list[str], list[str]]":
        songs_list = []
        songs_changes_list = []
        for playlist in self.playlists:
            playlist = rpl_bad_chars(playlist["name"])
            songs_list.append(str(self.user_path + "/" + playlist + "_songs.txt"))
            songs_changes_list.append(str(self.user_path + "/" + playlist + "_songs_changes.txt"))
        return songs_list, songs_changes_list

    def get_playlists(self):
        user_playlists = []
        try:
            playlists = self.spotify.user_playlists(self.id)
        except SpotifyException:
            pass

        for playlist in playlists["items"]:
            user_playlists.append(playlist)

        return user_playlists

    def get_playlist_names(self):
        playlist_names = []
        for pl in self.playlists:
            playlist_names.append(pl["name"])
        return playlist_names
