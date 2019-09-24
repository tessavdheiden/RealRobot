import gps
import time

FPS = 4
last_frame_time = 0
gps = gps.GPS()

init_longitude = None
init_latitude = None

key = input('Do you want to start the episode? (y/n)')

if key == 'y':
    while True:
        current_time = time.time()
        last_frame_time = current_time

        sleep_time = 1./FPS - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        if gps.is_ready:
            if not init_longitude or not init_longitude:
                init_longitude = gps.longitude
                init_latitude = gps.latitude
            else:
                print(float(gps.longitude) - float(init_longitude), float(gps.latitude) - float(init_latitude))


else:
    print('Episode is not started!')
