# spotify tracker
#
# to do:
#   - write comments
#   x debug HTTP 404 Error

import spotify_playlist_tracker as spt
import config
from datetime import datetime


def main():

    start = datetime.now()
    print(str(start)+"\n")
    print("Authenticating with Spotify...")
    scope = "playlist-modify-public"
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope=scope)
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
