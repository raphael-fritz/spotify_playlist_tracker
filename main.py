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
    
    print("Reading Usernames.txt ...", flush=True)
    usernames = spt.get_usernames()

    print("Acquiring User data...", flush=True)    
    for user in usernames:
        print(user["name"] + ": ")
        user = spt.get_spotify_user(spotify, user)
        spt.create_user_dir(user)
        spt.update_user_dir(user)
        print("-------------------------------------------------------------------------------")
    print("Success!\n")

    end = datetime.now()
    print("Elapsed time: ", (end-start))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
