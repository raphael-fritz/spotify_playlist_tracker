from spotipy import SpotifyException
from re import sub


def rpl_bad_chars(string: str) -> str:
    bad_chars = {"ä": "ae", "ö": "oe", "ü": "ue",
                 "Ä": "AE", "Ö": "OE", "Ü": "UE", "ß": "ss", ".": "_"}

    for char in bad_chars:
        string = string.replace(char, bad_chars[char])
    return sub(r"(\s)|([^\w\-_\.\ ])", "_", string)


class Spotify_Track:
    def __init__(self, track) -> None:
        self.name = track["track"]["name"]
        self.artist = track["track"]["artists"][0]["name"]
        self.artist_and_name = self.artist + "-" + self.name
        self.id = track["track"]["id"]
        self.added_at = track["added_at"]


class Spotify_Playlist:

    def __init__(self, spotify, name, uri):
        self.spotify = spotify
        self.uri = uri
        self.name = rpl_bad_chars(name)
        self.path = str(self.name + "_songs.txt")
        self.changes_path = str(self.name + "_songs_changes.txt")
        self.tracks = self._get_tracks()
        if not len(self.tracks):
            raise ValueError
        self.track_names = self._get_track_names()

    def _get_tracks(self) -> "list[Spotify_Track]":
        offset = 0
        tracks = []
        while True:
            response = self.spotify.playlist_items(self.uri,
                                                   offset=offset,
                                                   additional_types=['track'])

            if len(response['items']) == 0:
                break

            for item in response['items']:
                try:
                    if item["track"]["type"] == "track":
                        tracks.append(Spotify_Track(item))
                except (TypeError, AttributeError):
                    pass

            offset = offset + len(response['items'])
        return tracks

    def _get_track_names(self) -> "list[str]":
        track_names = []
        for track in self.tracks:
            track_names.append(track.artist_and_name)
        return track_names


class Spotify_User:

    def __init__(self, spotify, user_name, user_id):
        self.spotify = spotify
        self.name = user_name
        self.id = user_id
        self.playlists = self._get_playlists()
        self.playlist_names = self._get_playlist_names()
        self.user_path = str("data/" + rpl_bad_chars(self.name))
        self.pl_path = str(self.user_path + "/_playlists.txt")
        self.pl_changes_path = str(self.user_path + "/_playlists_changes.txt")
        self.song_path_list, self.song_changes_path_list = self._get_song_paths()

    def _get_playlists(self) -> "list[Spotify_Playlist]":
        user_playlists = []
        try:
            playlists = self.spotify.user_playlists(self.id)
        except SpotifyException:
            pass

        for playlist in playlists["items"]:
            try:
                user_playlists.append(Spotify_Playlist(
                    self.spotify, playlist["name"], playlist["uri"]))
            except ValueError:
                pass
        return user_playlists

    def _get_song_paths(self) -> "tuple[list[str], list[str]]":
        songs_list = []
        songs_changes_list = []
        for playlist in self.playlists:
            songs_list.append(str(self.user_path + "/" + playlist.path))
            songs_changes_list.append(
                str(self.user_path + "/" + playlist.changes_path))
        return songs_list, songs_changes_list

    def _get_playlist_names(self):
        playlist_names = []
        for pl in self.playlists:
            playlist_names.append(pl.name)
        return playlist_names
