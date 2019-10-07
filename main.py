import time
import support.firebase as fbdb
import support.util as util
import support.ultra_sound_drive as ultra_sound_drive

from support.gps import GPS
from support.controller import Controller
from model.episode import Episode
from model.model import ValueNetwork

db = fbdb.db

FPS_EPISODE = 2
FPS_CONTROLLER = 25
TIME_OUT_TIME = 25

load_value_network = False
mode = None

controller = Controller()

value_network = ValueNetwork()
if load_value_network:
    value_network.load_state_dict()

last_frame_time = 0
robot_gps = GPS('robot')
gamma = 0.9

init_longitude = None
init_latitude = None

robot_longitude = 0.0
robot_latitude = 0.0

init_robot_x = None
init_robot_y = None

def main():
    while True:
        if not mode:
            key = input('Do you want to start episode mode or free mode? (e/f)')
            if key == 'e':
                mode = 'EpisodeMode'
                print('Episode Mode activated')
            elif key == 'f':
                mode = 'FreeMode'
                print('Free Mode activated; Robot can be driven with the joystick')
            else:
                print('Non Buenos mode activated; Please try again')
        if mode == 'EpisodeMode':
            episode = Episode()
            init_longitude = None
            init_latitude = None
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
                            (init_robot_x, init_robot_y) = util.GPStoCartesian(init_longitude, init_latitude)
                            last_pos_x = 0.0
                            last_pos_y = 0.0
                        else:
                            robot_longitude = robot_gps.longitude
                            robot_latitude = robot_gps.latitude

                            pos_x, pos_y = util.GPStoCartesian(robot_longitude, robot_latitude)
                            vel_x, vel_y = util.CartesianSpeed(pos_x, pos_y, last_pos_x, last_pos_y)
                            (pos_x, pos_y) = (pos_x - init_robot_x, pos_y - init_robot_y)
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

                            last_pos_x = pos_x
                            last_pos_y = pos_y

                            if episode.step_number == TIME_OUT_TIME * FPS_EPISODE:
                                episode.uploadToServer(ending_message='Timeout')
                                break
                else:
                    time.sleep(0.5)
        if mode == 'FreeMode':
            while True:
                current_time = time.time()
                last_frame_time = current_time

                sleep_time = 1./25 - (current_time - last_frame_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                if controller.is_ready:
                    if controller.a:
                        ultra_sound_drive.forward_fast()
                        print("A pressed")
                    if controller.b:
                        ultra_sound_drive.backward()
                        print("B pressed")
                    if controller.degree:
                        print("Degree" + str(controller.degree))


main()