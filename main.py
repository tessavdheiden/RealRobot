import time
import logging
import support.firebase as fbdb
import support.util as util
#import support.gps_drive as gps_drive

from support.gps import GPS
from support.controller import Controller
from model.episode import Episode
#from model.model import ValueNetwork

db = fbdb.db

FPS_EPISODE = 0.5
FPS_CONTROLLER = 10
TIME_OUT_TIME = 25

load_value_network = False

controller = Controller()

#value_network = ValueNetwork(self_state_dim=8, mlp1_dims=[8, 100, 150], mlp2_dims=[150, 150], mlp3_dims=[150, 100, 64, 16, 1],
#                 attention_dims=150, cell_size=1, cell_num=4)
#if load_value_network:
#    value_network.load_state_dict()

last_frame_time = 0
robot_gps = GPS('robot')
gamma = 0.9

init_longitude = None
init_latitude = None

robot_longitude = 0.0
robot_latitude = 0.0

init_robot_x = None
init_robot_y = None

def main(mode=None):
    while True:
        if not mode:
            key = input('Do you want to start episode mode or free mode? (e-episode, f-free)')
            if key == 'e':
                mode = 'EpisodeMode'
                print('Episode Mode activated')
            elif key == 'f':
                mode = 'FreeMode'
                print('Free Mode activated; Robot can be driven with the joystick')
            else:
                print('Incorrect Input')
        if mode == 'EpisodeMode':
            episode = Episode()
            episode.resetEpisode()
            init_longitude = None
            init_latitude = None
            key = input('Do you want to start a new episode? (y/n)')
            if key == 'y':
                db.child('currentEpisode').remove()
                while True:

                    #check for phones connected
                    #main_robot_device = db.child('currentEpisode')
                    #humans = db.child('humans')

                    key = input('Please connect the phones you want to use during this episode. Press y-yes to continue, u-update to update the list or r-reset to reset the device list?')
                    if key == 'y':
                        if episode.key:
                            print('Episode with key: {} will start now!'.format(episode.key))
                            episode.episode_started = True
                            break
                    if key == 'r':
                        db.child('currentEpisode').remove()
                i = 0
                while True:
                    if episode.episode_started:
                        if episode.step_number % 10 == 0:
                            print('Current TimeStep is: {}', episode.step_number)
                        sleep_time = 1. / FPS_EPISODE
                        time.sleep(sleep_time)
                        #Testcodesnipped; can be deleted later.
                        # l =  [[0.3, 0.4],
                        #       [0.4, 0.3],
                        #       [0.5, 0.5],
                        #       [0.1, 0.6]
                        #       ]
                        # if i == len(l):
                        #     i = 0
                        # print(l[i])
                        # db.child('currentEpisode').child('action').update({'vx': l[i][0], 'vy': l[i][1]})
                        # i += 1

                        if not init_longitude or not init_latitude:
                            init_longitude = robot_gps.longitude
                            init_latitude = robot_gps.latitude
                            init_robot_x, init_robot_y = util.GPStoCartesian(init_longitude, init_latitude)
                            last_pos_x = 0.0
                            last_pos_y = 0.0
                        else:
                            robot_longitude = robot_gps.longitude
                            robot_latitude = robot_gps.latitude

                            robot_pos_x, robot_pos_y = util.GPStoCartesian(robot_longitude, robot_latitude)
                            robot_vel_x, robot_vel_y = util.CartesianSpeed(robot_pos_x, robot_pos_y, last_pos_x, last_pos_y)
                            robot_pos_x, robot_pos_y = robot_pos_x - init_robot_x, robot_pos_y - init_robot_y

                            #for user in connected_users:
                            #   check for speed, positions, etc.

                            reward = 0.0
                            if episode.checkGoalReached(pos_x=robot_pos_x, pos_y=robot_pos_y):
                                reward = 1.0

                            episode.incrementStepNumber()
                            episode.setPositions(robot_pos_x, robot_pos_y)
                            episode.setVelocities(robot_vel_x, robot_vel_y)
                            episode.setReward(reward=reward)

                            if reward:
                                episode.uploadToServer(ending_message='Reach Goal')
                                break

                            #Todo: get next action from firebase

                            last_pos_x = robot_pos_x
                            last_pos_y = robot_pos_y

                            if episode.step_number >= TIME_OUT_TIME * FPS_EPISODE:
                                episode.uploadToServer(ending_message='Timeout')
                                break
        if mode == 'FreeMode':
            while True:
                sleep_time = 1. / FPS_CONTROLLER
                if sleep_time > 0:
                    time.sleep(sleep_time)
                if controller.is_ready:
                    print(controller.a, controller.b, controller.degree)
                    #gps_drive.joystick_drive(controller.degree, controller.a, controller.b)


if __name__ == '__main__':
    main()