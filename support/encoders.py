import time, sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

EncodeL = 2
EncodeR = 3

GPIO.setup(EncodeL, GPIO.IN)
GPIO.setup(EncodeR, GPIO.IN)

# Left Wheel
CurRotL = 0
RotationsL = 0
LastL = 0
InL = 0

# Right
CurRotR = 0
RotationsR = 0
LastR = 0
InR = 0

Running = 1

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

def RPM_R():
    timestep = 0.2
    rot = 0
    t = time.clock()
    while t <= timestep:
        if InR == 0 and LastR == 1:
            rot += 1
    rpm = rot * 60/(timestep * 20)
    return rpm

def RPM_L():
    timestep = 0.2
    rot = 0
    t = time.clock()
    while t <= timestep:
        if InR == 0 and LastR == 1:
            rot += 1
    rpm = rot * 60/(timestep * 20)
    return rpm

while Running:
    InL = GPIO.input(EncodeL)
    InR = GPIO.input(EncodeR)

    if InL == 0 and LastL == 1:
        WheelL()

    if InR == 0 and LastR == 1:
        WheelR()

    LastL = InL
    LastR = InR

GPIO.cleanup()