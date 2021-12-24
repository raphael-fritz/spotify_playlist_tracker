from datetime import datetime, timedelta
from time import sleep
from main import main
from sys import argv

def scheduler():
    time_s = 24*3600
    try:
        if len(argv) > 1:
            if argv[1] == "-t":
                time_s = int(argv[2])
    except IndexError:
        print("Too few arguments!\nUsage: scheduler.py -t [seconds]")
        exit()

    td = timedelta(seconds=time_s)
    print("Scheduler will run main every " + str(td) + "\n")
    while True:
        try:
            main()
            print("Now sleeping until ", (datetime.now() + td))
            sleep(time_s)
        except KeyboardInterrupt:
            print("\nExiting scheduler...")
            exit()
        except Exception as e:
            with open("log.txt", "a+") as file:
                file.write(str(e))
                print(e)
                sleep(60)


if __name__ == "__main__":
    scheduler()
