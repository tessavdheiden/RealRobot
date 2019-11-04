import time, sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

EncodeL = 2
EncodeR = 3

GPIO.setup(EncodeL, GPIO.IN)
GPIO.setup(EncodeR, GPIO.IN)
GPIO.setwarnings(False)

# Left Wheel
CurRotL = 0
RotationsL = 0
LastL = 0
InL = 0
rpm_l = 0

# Right
CurRotR = 0
RotationsR = 0
LastR = 0
InR = 0
rpm_r = 0

Running = 1

t = time.time()

def WheelL():
    global CurRotL
    global RotationsL
    CurRotL = CurRotL + 1

    if CurRotL == 20:
        RotationsL = RotationsL + 1
        sys.stdout.write("Full Rotation: Left Wheel\n")
        sys.stdout.flush()
        CurRotL = 0

def WheelR():
    global CurRotR
    global RotationsR
    CurRotR = CurRotR + 1

    if CurRotR == 20:
        RotationsR = RotationsR + 1
        sys.stdout.write("Full Rotation: Right Wheel\n")
        sys.stdout.flush()
        CurRotR = 0

def RPM():
    EncodeL = 2
    EncodeR = 3

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EncodeL, GPIO.IN)
    GPIO.setup(EncodeR, GPIO.IN)
    GPIO.setwarnings(False)

    
    global InR
    global LastR
    InR = GPIO.input(EncodeR)
    global InL
    global LastL
    InL = GPIO.input(EncodeL)
    global t
    global rpm_r
    global rpm_l
    timestep = 0.8
    rot_r = 0
    rot_l = 0
    while time.time()-timestep <= t:
        if InR == 0 and LastR == 1:
            rot_r += 1
        if InL == 0 and LastL == 1:
            rot_l += 1
        LastR = InR
        LastL = InL
    t = time.time()
    rpm_r = rot_r * 60/(timestep * 20)
    rpm_l = rot_l * 60/(timestep * 20)
    print(rpm_r)

"""while Running:
    InL = GPIO.input(EncodeL)
    InR = GPIO.input(EncodeR)

    if InL == 0 and LastL == 1:
        WheelL()

    if InR == 0 and LastR == 1:
        WheelR()

    LastL = InL
    LastR = InR"""

GPIO.cleanup()