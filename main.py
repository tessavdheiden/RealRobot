import time
import argparse

from gps import GPS

parser = argparse.ArgumentParser('Parse configuration file')
parser.add_argument('human1', default=False, action='store_false')
parser.add_argument('human2', default=False, action='store_false')
parser.add_argument('human3', default=False, action='store_false')
parser.add_argument('human4', default=False, action='store_false')
parser.add_argument('human5', default=False, action='store_false')
args = parser.parse_args()

FPS = 4
last_frame_time = 0
robot_gps = GPS('robot')
human1_gps = None
human2_gps = None
human3_gps = None
human4_gps = None
human5_gps = None
if args.human1:
    human1_gps = GPS('human1')
if args.human2:
    human2_gps = GPS('human2')
if args.human3:
    human3_gps = GPS('human3')
if args.human4:
    human4_gps = GPS('human4')
if args.human5:
    human5_gps = GPS('human5')

init_longitude = None
init_latitude = None

robot_longitude = 0.0
robot_latitude = 0.0
human1_longitude = 0.0
human1_latitude = 0.0
human2_longitude = 0.0
human2_latitude = 0.0
human3_longitude = 0.0
human3_latitude = 0.0
human4_longitude = 0.0
human4_latitude = 0.0
human5_longitude = 0.0
human5_latitude = 0.0

key = input('Do you want to start the episode? (y/n)')

if key == 'y':
    while True:
        current_time = time.time()
        last_frame_time = current_time

        sleep_time = 1./FPS - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        if robot_gps.is_ready:
            if not init_longitude or not init_longitude:
                init_longitude = robot_gps.longitude
                init_latitude = robot_gps.latitude
            else:
                robot_longitude = robot_gps.longitude - init_longitude
                robot_latitude = robot_gps.latitude - init_latitude
                if human1_gps:
                    human1_longitude = human1_gps.longitude - init_longitude
                    human1_latitude = human1_gps.latitude - init_latitude
                if human2_gps:
                    human2_longitude = human2_gps.longitude - init_longitude
                    human2_latitude = human2_gps.latitude - init_latitude
                if human3_gps:
                    human3_longitude = human3_gps.longitude - init_longitude
                    human3_latitude = human3_gps.latitude - init_latitude
                if human4_gps:
                    human4_longitude = human4_gps.longitude - init_longitude
                    human4_latitude = human4_gps.latitude - init_latitude
                if human5_gps:
                    human5_longitude = human5_gps.longitude - init_longitude
                    human5_latitude = human5_gps.latitude - init_latitude
else:
    print('Episode is not started!')
