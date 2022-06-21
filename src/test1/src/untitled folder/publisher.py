#!/usr/bin/env python3
import rospy 
import time 
from std_msgs.msg import String

pub=rospy.Publisher('chatter',String,queue_size=10)

rospy.init_node('talker',anonymous=True) 

rate=rospy.Rate(10)

def counter(string):
  new_string = string.split()
  return len(new_string)

i=0

while i<1:
  print(" Enter String ")
  str1 = input()
  length = counter(str1)
  print(" Number of words is : ")
  rospy.loginfo(length)
  pub.publish(str(length))
  rate.sleep()
  i= i + 1
