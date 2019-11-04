import RPi.GPIO as GPIO          
from time import sleep

in1b = 24
in2b = 23
enb = 12
in1a = 27
in2a = 17
ena = 13
temp1=1

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(in1b,GPIO.OUT)
GPIO.setup(in2b,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.setup(in1a,GPIO.OUT)
GPIO.setup(in2a,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)

GPIO.output(in1a,GPIO.LOW)
GPIO.output(in2a,GPIO.LOW)
GPIO.output(in1b,GPIO.LOW)
GPIO.output(in2b,GPIO.LOW)
pa=GPIO.PWM(ena,1000)
pb=GPIO.PWM(enb,1000)


pa.start(59)
pb.start(0)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):

    # x=raw_input()
    GPIO.output(in1b,GPIO.HIGH)
    GPIO.output(in2b,GPIO.LOW)
    GPIO.output(in1a,GPIO.HIGH)
    GPIO.output(in2a,GPIO.LOW)
    
    """if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")"""