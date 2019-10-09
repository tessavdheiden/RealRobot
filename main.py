import time
import support.firebase as fbdb
import support.util as util
import support.gps_drive as gps_drive

from support.gps import GPS
from support.controller import Controller
from model.episode import Episode
#from model.model import ValueNetwork

db = fbdb.db

FPS_EPISODE = 2
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
            key = input('Do you want to start episode mode or free mode? (e/f)')
            if key == 'e':
                mode = 'EpisodeMode'
                print('Episode Mode activated')
            elif key == 'f':
                mode = 'FreeMode'
                print('Free Mode activated; Robot can be driven with the joystick')
        if mode == 'EpisodeMode':
            episode = Episode()
            init_longitude = None
            init_latitude = None
            while True:
                if episode.episode_started:
                    print('Episode is started!' + str(episode.step_number))
                    sleep_time = 1. / FPS_EPISODE
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                        if not init_longitude or not init_latitude:
                            init_longitude = robot_gps.longitude
                            init_latitude = robot_gps.latitude
                            (init_robot_x, init_robot_y) = util.GPStoCartesian(init_longitude, init_latitude)
                            last_pos_x = 0.0
                            last_pos_y = 0.0
                        else:
                            robot_longitude = robot_gps.longitude
                            robot_latitude = robot_gps.latitude

                            pos_x, pos_y = util.GPStoCartesian(robot_longitude, robot_latitude)
                            vel_x, vel_y = util.CartesianSpeed(pos_x, pos_y, last_pos_x, last_pos_y)
                            pos_x, pos_y = pos_x - init_robot_x, pos_y - init_robot_y
                            reward = 0.0
                            if episode.checkGoalReached(pos_x=pos_x, pos_y=pos_y):
                                reward = 1.0

                            episode.incrementStepNumber()
                            episode.setPositions(pos_x, pos_y)
                            episode.setVelocities(vel_x, vel_y)
                            episode.setReward(reward=reward)

                            if reward:
                                episode.uploadToServer(ending_message='Reach Goal')
                                break
                            
                            #get next action from firebase

                            last_pos_x = pos_x
                            last_pos_y = pos_y

                            if episode.step_number == TIME_OUT_TIME * FPS_EPISODE:
                                episode.uploadToServer(ending_message='Timeout')
                                break
                else:
                    time.sleep(0.5)
        if mode == 'FreeMode':
            while True:
                sleep_time = 1. / FPS_CONTROLLER
                if sleep_time > 0:
                    time.sleep(sleep_time)
                if controller.is_ready:
                    print(controller.a, controller.b, controller.degree)
                    gps_drive.joystick_drive(controller.degree, controller.a, controller.b)


main()