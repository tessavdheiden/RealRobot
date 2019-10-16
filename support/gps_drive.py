import time
#from gpiozero import Motor
from support.gpio_sim import Motor
from support.gps import GPS
import RPi.GPIO as GPIO
from enum import Enum

in1b = 24
in2b = 23
enb = 12
in1a = 27
in2a = 17
ena = 13

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup

GPIO.setup(in1b, GPIO.OUT)
GPIO.setup(in2b, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.setup(in1a, GPIO.OUT)
GPIO.setup(in2a, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)

GPIO.output(in1a, GPIO.LOW)
GPIO.output(in2a, GPIO.LOW)
GPIO.output(in1b, GPIO.LOW)
GPIO.output(in2b, GPIO.LOW)
pa = GPIO.PWM(ena, 1000)
pb = GPIO.PWM(enb, 1000)

pa.start(100)
pb.start(100)

class Go(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2


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

# motor1 = Motor(23, 24)
# motor2 = Motor(17, 27)

def fwd(vl,vr):
    pa.start(vl)
    pb.start(vr)
    GPIO.output(in1b, GPIO.HIGH)
    GPIO.output(in2b, GPIO.LOW)
    GPIO.output(in1a, GPIO.HIGH)
    GPIO.output(in2a, GPIO.LOW)

def bwd(vl,vr):
    pa.start(vl)
    pb.start(vr)
    GPIO.output(in1b, GPIO.LOW)
    GPIO.output(in2b, GPIO.HIGH)
    GPIO.output(in1a, GPIO.LOW)
    GPIO.output(in2a, GPIO.HIGH)

def stop():
    pa.start(0)
    pb.start(0)

""" def left():
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
    motor1.backward(.5) """

def joystick_drive(angle: float, forward: bool, backward: bool):
    motor_left = 100
    motor_right = 100
    if angle < 0.0:
        motor_left -= abs(angle) * 100 / 3.14
    elif angle > 0.0:
        motor_right -= abs(angle) * 100 / 3.14
    print(motor_left, motor_right)
    if forward:
        fwd(motor_left, motor_right)
    elif backward:
        bwd(motor_left, motor_right)
    else:
        stop()
    
def nn_drive(motorLeft: float, motorRight: float, Mode : Go=0):
    if Mode == 1:
        fwd(motorLeft, motorRight)
    elif Mode == 2:
        fwd(motorLeft, motorRight)
    else:
        stop()





