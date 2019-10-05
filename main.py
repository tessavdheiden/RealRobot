import time
import support.firebase as fbdb
import support.util as util

from support.gps import GPS
from support.controller import Controller
from model.episode import Episode

#import ultra_sound_drive

db = fbdb.db

FPS_EPISODE = 2
FPS_CONTROLLER = 25

controller = Controller()

last_frame_time = 0
robot_gps = GPS('robot')

init_longitude = None
init_latitude = None

robot_longitude = 0.0
robot_latitude = 0.0

def main():
    while True:
        key = input('Do you want to start episode mode? (y/n)')
        if key == 'y':
            episode = Episode()
            init_longitude = None
            init_latitude = None
            #listener
            while True:
                if episode.episode_started:
                    print('Episode is started!' + str(episode.step_number))
                    current_time = time.time()
                    last_frame_time = current_time
                    sleep_time = 1. / FPS_EPISODE - (current_time - last_frame_time)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                        if not init_longitude or not init_latitude:
                            init_longitude = robot_gps.longitude
                            init_latitude = robot_gps.latitude
                            last_pos_x = 0.0
                            last_pos_y = 0.0
                        else:
                            robot_longitude = robot_gps.longitude - init_longitude
                            robot_latitude = robot_gps.latitude - init_latitude

                            pos_x, pos_y = util.GPStoCartesian(robot_longitude, robot_latitude)
                            vel_x, vel_y = util.CartesianSpeed(pos_x, pos_y, last_pos_x, last_pos_y)

                            episode.incrementStepNumber()
                            episode.setPositions(pos_x, pos_y)
                            episode.setVelocities(vel_x, vel_y)

                            last_pos_x = pos_x
                            last_pos_y = pos_y

                            if episode.step_number == 50:
                                episode.uploadToServer()
                                break
                    # if episode.episode_ended:
                    #     episode.uploadToServer()
                    #     print('Episode ended')
                    #     break
                else:
                    time.sleep(0.5)
        else:
            print('Episode is not started! Robot can be driven by Controller')
            while True:
                current_time = time.time()
                last_frame_time = current_time

                sleep_time = 1./25 - (current_time - last_frame_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                if controller.is_ready:
                    if controller.a:
                        #ultra_sound_drive.forward_fast()
                        print("A pressed")
                    if controller.b:
                        #ultra_sound_drive.backward()
                        print("B pressed")
                    if controller.degree:
                        print("Degree" + str(controller.degree))

main()