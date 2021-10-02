# spotify tracker
#
# to do:
#   x writing out changes in playlists, output should look something like this:
#       time
#          user1:
#               + playlist 2
#               - playlist 1
#          user2:
#               ...
#   x implement change tracking for removals
#       -> implement + and - as indicators for addition/removal
#   - apply all tracking for playlists to songs in playlists
#   x cleanup
#   - more cleanup
#   x check paths for bad chars

import time
import datetime
import config
import spotify_playlist_tracker as spt


def main():

    print(datetime.datetime.fromtimestamp(time.time()))
    
    # authenticate with spotify
    scope = "playlist-modify-public"
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope=scope)    
    user_list = spt.get_spotify_users(spotify)
    
    spt.create_dir_structure(user_list)
    spt.update_dir_structure(user_list)


if __name__ == "__main__":
    main()
