# spotify tracker
#
# to do:
#   - write comments
#   x add tracking for individual playlists
#   - move to event driven structure
#   - multithreading

from os import error
import spotipy
import config
import spotify_playlist_tracker as spt
from datetime import datetime, timedelta
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
        print("Authentication Error!\n", flush=True)
        exit()


    spt.check_dir("data")
    """
    playlists = spt.get_playlists("playlists.txt")
    try:
        for playlist in progressBar(playlists, prefix="Acquiring Playlist data:\t", suffix="done", length=50):
            playlist = spt.get_spotify_pl(spotify, playlist)
            spt.create_pl_dir(playlist)
            spt.update_pl_dir(playlist)
    except ZeroDivisionError:
        print("playlists.txt is empty")
    """

    user = spt.get_spotify_user(spotify, {"name":"maflra", "id":"maflra"})
    spt.create_user_dir(user)
    spt.update_user_dir(user)
    with open("log.txt", "a+",encoding="utf-8") as file:
        file.write("-------------------------------------\n")
        for change in spt.read_user_dir(user, start_date=(datetime.now()-timedelta(hours=12))):
            file.write(change)
            print(change)

    usernames = spt.get_usernames("usernames.txt")
    with open("log2.txt", "w+", encoding="utf-8") as f:
        for user in usernames:
            user = spt.get_spotify_user(spotify, user)
            f.write("\n"+user.name+": ")
            for change in spt.read_user_dir(user, start_date=(datetime.now()-timedelta(hours=12))):
                try:
                    f.write(change)
                    print(change)
                except UnicodeEncodeError:
                    print("error")
                    pass

    """
    try:
        for user in progressBar(usernames, prefix="Acquiring User data:\t\t", suffix="done", length=50):
            user = spt.get_spotify_user(spotify, user)
            spt.create_user_dir(user)
            spt.update_user_dir(user)
    except ZeroDivisionError:
        print("usernames.txt is empty")"""


def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='x', printEnd="\r"):
    """
    Credit to https://stackoverflow.com/users/9761768/diogo

    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function

    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


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
