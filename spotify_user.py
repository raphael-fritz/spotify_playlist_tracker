from spotipy import SpotifyException


class Spotify_Playlist:

    def __init__(self, spotify, uri):
        self.spotify = spotify
        self.uri = uri
        self.tracks = self.get_tracks()
        if not len(self.tracks):
            raise Exception


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

    def get_playlists(self):
        user_playlists = []
        try:
            playlists = self.spotify.user_playlists(self.id)
        except SpotifyException:
            pass

        for playlist in playlists["items"]:
            user_playlists.append(playlist)

        return user_playlists
