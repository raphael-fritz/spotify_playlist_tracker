# spotify tracker
#
# to do:
#   - write comments
#   - add tracking for individual playlists
#   - move to event driven structure

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
    print(str(start)+"\n")

    print("Authenticating with Spotify...")
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope="playlist-modify-public", openBrowser=headless)
    user_list = spt.get_spotify_users(spotify)

    print("Creating/checking directory structure...")
    spt.create_dir_structure(user_list)

    print("Updating directory structure...\n")
    spt.update_dir_structure(spotify, user_list)

    end = datetime.now()
    print("Finished!")
    print("Elapsed time: ", (end-start))


if __name__ == "__main__":
    main()
