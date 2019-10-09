import time
from threading import Event
import support.firebase as fbdb
import support.util as util
from model.episode import Episode
from support.gps_drive import Go, nn_drive



def main():
    db = fbdb.db
    episode = Episode()
    while True:
        while episode.episode_started:
            actionDict = db.child('currentEpisode').child('action').get().val()
            (vx, vy) = (actionDict['vx'], actionDict['vy'])

            if vx < vy:
                motorLeft = .5
                motorRight = .75
                mode = 1
            elif vx > vy:
                motorLeft = .75
                motorRight = .5
                mode = 2
            elif vx == vy and vx > 0:
                motorLeft = .75
                motorRight = .5
                mode = 1
            elif vx == vy and vx < 0:
                motorLeft = .75
                motorRight = .5
                mode = 2
            else:
                motorLeft = .0
                motorRight = .0
                mode = 0

            print("vx = {}, vy = {}".format(vx, vy))
            nn_drive(motorLeft, motorRight, mode)
            time.sleep(1)

if __name__ == '__main__':
    main()
    event = Event()
