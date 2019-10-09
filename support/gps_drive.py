import time
from gpiozero import Motor
from support.gps import GPS

# ------- CONTROL -------
LON_RANGE = 10
LAT_RANGE = 10

# ------- GPS -------
FPS = 4
last_frame_time = 0
robot_gps = GPS('robot')

init_longitude = None
init_latitude = None

robot_longitude = 0.0
robot_latitude = 0.0

# ------- DRIVE -------

motor1 = Motor(23, 24)
motor2 = Motor(27, 17)

def fwd():
    motor1.forward(.5)
    motor2.forward(.5)

def bwd():
    motor1.backward(.5)
    motor2.backward(.5)

def left():
    motor1.forward(.75)
    motor2.forward(.5)
    
def right():
    motor2.forward(.75)
    motor1.forward(.5)
    
def rot_clock():
    motor1.forward(.5)
    motor2.backward(.5)

def rot_counter_clock():
    motor2.forward(.5)
    motor1.backward(.5)

def joystick_drive(angle: float, forward: bool, backward: bool):
    motor_left = 0.5
    motor_right = 0.5
    if angle < 0.0:
        motor_left -= abs(angle) * 0.5 / 3.14
    elif angle > 0.0:
        motor_right -= abs(angle) * 0.5 / 3.14
    if forward:
        motor1.forward(motor_left)
        motor2.forward(motor_right)
    elif backward:
        motor1.backward(motor_left)
        motor2.backward(motor_right)
    
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
                if robot_longitude > LON_RANGE and robot_latitude < LAT_RANGE:
                    fwd()
                elif robot_latitude > LAT_RANGE and robot_longitude < LON_RANGE:
                    bwd()
                elif robot_longitude > LON_RANGE and robot_latitude > LAT_RANGE:
                    left()
                else:
                    right()
                time.sleep(2)
                motor1.stop()
                motor2.stop() 

else:
    print('Episode is not started!')
    


