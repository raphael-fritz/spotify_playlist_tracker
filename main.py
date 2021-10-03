# spotify tracker
#
# to do:
#   - write comments
#   x debug HTTP 404 Error

import time
import datetime
import config
import spotify_playlist_tracker as spt


def main():

    start = datetime.datetime.fromtimestamp(time.time())
    print(str(start)+"\n")
    print("Authenticating with Spotify...")
    # authenticate with spotify
    scope = "playlist-modify-public"
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope=scope)
    user_list = spt.get_spotify_users(spotify)

    print("Creating/checking directory structure...")
    spt.create_dir_structure(user_list)

    print("Updating directory structure...")
    spt.update_dir_structure(spotify, user_list)

    end = datetime.datetime.fromtimestamp(time.time())
    print("Finished!")
    print("Elapsed time: ", str(end-start))


if __name__ == "__main__":
    main()
