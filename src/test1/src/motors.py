#!/usr/bin/env python3
import os
import threading
import RPi.GPIO as GPIO
import rospy
#import math
import time
from std_msgs.msg import String
from test1.msg import sensor_output

in1 = 17
in2 = 22
ena = 16

in3 = 23
in4 = 24
enb = 20

temp1=1

#global TIME_LIMIT
TIME_LIMIT = 15.0
#global side
side = ''
#global distance
distance = 100

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p1=GPIO.PWM(ena,1000)
p2=GPIO.PWM(enb,1000)

def shutdown():
    print('Quitting.')
    cleanup()
    nodes = os.popen("rosnode list").readlines()
    for i in range(len(nodes)):
        nodes[i] = nodes[i].replace("\n","")
    for node in nodes:
        os.system("rosnode kill "+ node)
    #quit()

def start():
    global distance
    global TIME_LIMIT
    timer = threading.Timer(TIME_LIMIT, shutdown)
    timer.start()
    p1.start(37)
    p2.start(50)
    while(True):
        forward()
        current_distance = distance
        #if current_distance != distance:
        #    print('yes')
        if current_distance < 30:
            found_object()
            stop()
            time.sleep(0.2)
            print(current_distance)
        if current_distance != distance:
            print('yes')

def distance_callback(msg):
	#print('LEFT:', msg.left_distance)
	#print('RIGHT:', msg.right_distance)
	global distance
	#distance = min(msg.left_distance, msg.right_distance)
	print(msg.left_distance, msg.right_distance)
	if abs(msg.left_distance - msg.right_distance) <= 20:
	    distance = min(msg.left_distance, msg.right_distance)
def found_object():
    stop()
    time.sleep(4)
    global side
    if side == 'right':
        right()
        print('going')
    elif side == 'left':
        left()
        print('going')

def image_callback(msg):
	#print('SIDE:', msg.data)
	#return_arrow(msg.data)
	global side
	side = msg.data
	
def return_arrow(side):
    return side
	
def forward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    #print("forward")

def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    print("stop")
    
def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    print("backward")
    
def right():
    high()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(0.42)
    print("right")
    #time.sleep(0.2)
    medium()

def left():
    high()
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    time.sleep(0.42)
    print("left")
    #time.sleep(0.2)
    medium()

def low():
    p1.ChangeDutyCycle(19)
    p2.ChangeDutyCycle(25)

def medium():
    p1.ChangeDutyCycle(40)
    p2.ChangeDutyCycle(50)

def high():
    p1.ChangeDutyCycle(56)
    p2.ChangeDutyCycle(75)

def cleanup():
    GPIO.cleanup()

def main():
    move()
    
def move():
    while not rospy.is_shutdown():
        rospy.init_node('motors', anonymous = 'True')
        Sub=rospy.Subscriber('/distance', sensor_output, distance_callback)
        Sub=rospy.Subscriber('/arrow', String, image_callback)
        start()
    
if __name__ == '__main__':
    main()
