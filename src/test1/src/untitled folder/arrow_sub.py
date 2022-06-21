#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback(msg):
	print(msg.data)
	
rospy.init_node('arrow',anonymous = 'True')
Sub=rospy.Subscriber('/arrow', String, callback)
rospy.spin()
