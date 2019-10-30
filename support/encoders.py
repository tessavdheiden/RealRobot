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

while Running:
    InL = GPIO.input(EncodeL)
    InR = GPIO.input(EncodeR)

    if InL == 0 and LastL == 1:
        WheelL()
        sys.stdout.write("L\n")
        sys.stdout.flush()

    if InR == 0 and LastR == 1:
        WheelR()
        sys.stdout.write("R\n")
        sys.stdout.flush()

    LastL = InL
    LastR = InR

GPIO.cleanup()