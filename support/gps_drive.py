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
motor2 = Motor(17, 27)

def fwd():
    motor1.forward(.75)
    motor2.forward(.75)

def bwd():
    motor1.backward(.75)
    motor2.backward(.75)

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
    motor_left = 1.0
    motor_right = 1.0
    if angle < 0.0:
        motor_left -= abs(angle) * 1.0 / 3.14
    elif angle > 0.0:
        motor_right -= abs(angle) * 1.0 / 3.14
    print(motor_left, motor_right)
    if forward:
        motor1.forward(motor_left)
        motor2.forward(motor_right)
    elif backward:
        motor1.backward(motor_left)
        motor2.backward(motor_right)
    else:
        motor1.stop()
        motor2.stop()
    


