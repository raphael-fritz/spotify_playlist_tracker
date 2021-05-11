# Spotify Playlist Tracker
A simple Python programm to track the playlists and the tracks in them of a given list of users.

## Installation
* Install Spotipy with `pip install spotipy`.

* Create a file called `config.py` the contens of which should look like this:
    ```python
    client_id       =   "xxxxxx_spotify_client_id_xxxxxxx"
    client_secrect  =   "xxxx_spotify_client_secrect_xxxx"
    redirect_uri    =   "http://example.com"
    ```
    For further information on these parameters look into the [Spotipy Authorization-Code-Flow Documentation](https://spotipy.readthedocs.io/en/2.18.0/#getting-started) or the [Spotify Web API Authorization-Guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/).

* Create a file called `usernames.txt` the contents of which should look like this:
    ```
    username1 user_id1
    username2 user_id2
    ...
    ```
    The Username and User-Id can be separated by a space, tab, multiple spaces or multiple tabs.
    The Username can be anything you want but it must not include spaces or dots! 

## Usage
Run the programm with `py main.py` or similar.

