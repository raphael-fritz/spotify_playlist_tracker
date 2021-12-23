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
from progressBar import progressBar
from sys import argv


def main(headless=False):
    if len(argv) > 1:
        if argv[1] == "-headless":
            headless = True
    if headless == True:
        print("Headless-Mode enabled")

    print("Authenticating with Spotify:", end="\t")
    spotify = spt.spotify_authentication(
        config.client_id, config.client_secrect, config.redirect_uri, scope="playlist-modify-public", openBrowser=headless)
    if type(spotify) == spotipy.client.Spotify:
        print(" Success!")
    else:
        print("Authentication Error!", flush=True)
        exit()

    usernames = []
    with open("usernames.txt") as username_list:
        for username in progressBar(username_list.readlines(), prefix="Reading Usernames.txt:\t\t", suffix="done", length=50):
            (name, id) = username.split()
            user = {
                "name": name,
                "id": id
            }
            usernames.append(user)

    for user in progressBar(usernames, prefix="Acquiring User data:\t\t", suffix="done", length=50):
        user = spt.get_spotify_user(spotify, user)
        spt.create_user_dir(user)
        spt.update_user_dir(user)


if __name__ == "__main__":
    print("Starting Time: ", datetime.now(),"\n")
    start = datetime.now()
    try:
        main()

    except KeyboardInterrupt:
        print("\nElapsed time: ", str(datetime.now()-start), flush=True)
        exit()

    finally:
        print("\nElapsed time: ", str(datetime.now()-start), flush=True)
        exit()

