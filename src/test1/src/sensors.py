#! /usr/bin/env python3

import rospy
import RPi.GPIO as GPIO
import time
import math
from test1.msg import sensor_output

GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER_LEFT = 2
GPIO_ECHO_LEFT = 3
GPIO_TRIGGER_RIGHT = 6
GPIO_ECHO_RIGHT = 13

GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)
 
#PUBLISHER NODE 
pub=rospy.Publisher('/distance', sensor_output, queue_size=100)

rospy.init_node('sensor', anonymous=True)  

rate=rospy.Rate(5)

def distance():
    '''
    LEFT
    '''
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_LEFT, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_LEFT, False)
 
    StartTime_LEFT = time.time()
    StopTime_LEFT = time.time()
 
    # save StartTime left
    while GPIO.input(GPIO_ECHO_LEFT) == 0:
        StartTime_LEFT = time.time()
 
    # save time of arrival left
    while GPIO.input(GPIO_ECHO_LEFT) == 1:
        StopTime_LEFT = time.time()
        
    '''
    RIGHT
    '''
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_RIGHT, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_RIGHT, False)
    
    StartTime_RIGHT = time.time()
    StopTime_RIGHT = time.time()
    
    
    # save StartTime right
    while GPIO.input(GPIO_ECHO_RIGHT) == 0:
        StartTime_RIGHT = time.time()
 
    # save time of arrival right
    while GPIO.input(GPIO_ECHO_RIGHT) == 1:
        StopTime_RIGHT = time.time()
        
    
    # time difference between start and arrival
    TimeElapsed_LEFT = StopTime_LEFT - StartTime_LEFT
    TimeElapsed_RIGHT = StopTime_RIGHT - StartTime_RIGHT
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_LEFT = math.floor((TimeElapsed_LEFT * 34300) / 2)
    distance_RIGHT = math.floor((TimeElapsed_RIGHT * 34300) / 2)
 
    #return distance_LEFT
    return (distance_LEFT, distance_RIGHT)
 
if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            #rospy.loginfo(dist)
            print(dist)
            output = sensor_output()
            output.left_distance = dist[0]
            output.right_distance = dist[1]
            pub.publish(output)
            rate.sleep()
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    GPIO.cleanup()
