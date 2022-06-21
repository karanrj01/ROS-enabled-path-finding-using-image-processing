#! /usr/bin/env python3

import rospy
import time
from test1.msg import sensor_output

def callback(msg):
	print('LEFT:', msg.left_distance)
	print('RIGHT:', msg.right_distance)

rospy.init_node('listener', anonymous = 'True')
Sub=rospy.Subscriber('distance', sensor_output, callback)
rospy.spin()
