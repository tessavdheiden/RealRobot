import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# ULTRA SOUND
TRIG = 4
ECHO = 18

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    #CM:
    distance = sig_time / 0.000058
    return distance

# DRIVE
in1 = 24
in2 = 23

in3 = 17
in4 = 27

en = 25
temp1=1

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p=GPIO.PWM(en,1000)
p.start(25)

def forward():
    print("forward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)

def forward_fast():
    print("fast")
    p.ChangeDutyCycle(75)
    forward()

def forward_slow():
    print("slow")
    p.ChangeDutyCycle(50)
    forward()

def stop():
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)

def backward():
    print("backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)

while True:
    distance = get_distance()
    time.sleep(0.05)
    print(distance)
    
    print("s-stop e-exit r-run")
    x = input()
    if x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
    elif x=='s':
        stop()
    elif x=='r':
        distance = get_distance()
        if distance >= 30:
            forward_fast()
        elif 30 > distance > 10:
            forward_slow()
        elif 10 >= distance > 5:
            stop()
        elif distance <= 5:
            backward()
