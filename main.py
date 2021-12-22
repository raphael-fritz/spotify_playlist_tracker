# spotify tracker
#
# to do:
#   - write comments
#   - add tracking for individual playlists
#   - move to event driven structure

import spotipy
import config
import spotify_playlist_tracker as spt
from datetime import datetime
from sys import argv


def main(headless=False):
    if len(argv) > 1:
        if argv[1] == "-headless":
            headless = True
    if headless == True:
        print("Headless-Mode enabled")

    start = datetime.now()

    print("Authenticating with Spotify...", end="\t", flush=True)
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope="playlist-modify-public", openBrowser=headless)
    if type(spotify) == spotipy.client.Spotify:
        print("Success!")
    else:
        print("Authentication Error!", flush=True)
        exit()
    
    print("Acquiring User data...", end="\t", flush=True)
    user_list = spt.get_spotify_users(spotify)
    print("\nSuccess!")

    print("Creating/checking directory structure...", end="\t", flush=True)
    spt.create_dir_structure(user_list)
    print("Success!")

    print("Updating directory structure...", flush=True)
    spt.update_dir_structure(spotify, user_list)

    end = datetime.now()
    print("Success!\n")
    print("Elapsed time: ", (end-start))


if __name__ == "__main__":
    main()
