# spotify tracker
#
# to do:
#   - write comments
#   x add tracking for individual playlists
#   - move to event driven structure

import spotipy
import config
import spotify_playlist_tracker as spt
import spotify_user as spu
from datetime import datetime
from progressBar import progressBar
from sys import argv


def track_users(spotify):
    usernames = []
    with open("usernames.txt") as username_list:
        for username in progressBar(username_list.readlines(), prefix="Reading Usernames.txt:\t\t\t", suffix="done", length=50):
            (name, id) = username.split()
            user = {
                "name": name,
                "id": id
            }
            usernames.append(user)

    for user in progressBar(usernames, prefix="Acquiring User data:\t\t\t", suffix="done", length=50):
        user = spt.get_spotify_user(spotify, user)
        spt.create_user_dir(user)
        spt.update_user_dir(user)
    print()


def track_playlists(spotify):
    playlists = []
    with open("playlists.txt") as playlist_list:
        for playlist in progressBar(playlist_list.readlines(), prefix="Reading Playlists.txt:\t\t\t", suffix="done", length=50):
            (name, id) = playlist.split()
            playlist = {
                "name": name,
                "id": id
            }
            playlists.append(playlist)

    for playlist in progressBar(playlists, prefix="Acquiring Playlist data:\t\t", suffix="done", length=50):
        playlist = spt.get_spotify_pl(spotify, playlist)
        spt.create_pl_dir(playlist)
        spt.update_pl_dir(playlist)
    print()


def main(headless=False):
    if len(argv) > 1:
        if argv[1] == "-headless":
            headless = True
    if headless == True:
        print("Headless-Mode enabled")

    print("Authenticating with Spotify:", end="\t\t")
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope="playlist-modify-public", openBrowser=headless)
    if type(spotify) == spotipy.client.Spotify:
        print(" Success!\n")
    else:
        print("Authentication Error!\n", flush=True)
        exit()

    spt.check_dir("data")
    track_playlists(spotify)
    track_users(spotify)


if __name__ == "__main__":
    print("Starting Time: ", datetime.now(), "\n")
    start = datetime.now()
    try:
        main()
        print("\nElapsed time: ", str(datetime.now()-start), flush=True)
        exit()

    except KeyboardInterrupt:
        print("\nElapsed time: ", str(datetime.now()-start), flush=True)
        exit()
