# spotify tracker
#
# to do:
#   - write comments

import time
import datetime
import config
import spotify_playlist_tracker as spt


def main():

    print(datetime.datetime.fromtimestamp(time.time()))
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

    print("Finished!")


if __name__ == "__main__":
    main()
