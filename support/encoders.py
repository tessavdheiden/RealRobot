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


def main():
    while Running:
        """InL = GPIO.input(EncodeL)
        InR = GPIO.input(EncodeR)

        if InL == 0 and LastL == 1:
            WheelL()

        if InR == 0 and LastR == 1:
            WheelR()
            print("DEBUG")

        LastL = InL
        LastR = InR"""
        
        # RPM
        t = time.time()
        LastL = 0
        LastR = 0
        
        timestep = 1
        rot_r = 0
        rot_l = 0
        while time.time()-timestep <= t:
            InL = GPIO.input(EncodeL)
            InR = GPIO.input(EncodeR)
            if InR == 0 and LastR == 1:
                rot_r += 1
            if InL == 0 and LastL == 1:
                rot_l += 1
            LastR = InR
            LastL = InL
        t = time.time()
        rpm_r = rot_r * 60/(timestep * 20)
        rpm_l = rot_l * 60/(timestep * 20)
        data = [rot_l, rot_r]
        print(data)


if __name__ == '__main__':
    main()


GPIO.cleanup()