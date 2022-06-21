#!/usr/bin/env python3

# Python libs
import sys, time

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2
from cv_bridge import CvBridge, CvBridgeError 
# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import Image
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

#VERBOSE=False
vid = cv2.VideoCapture(0, cv2.CAP_V4L)
bridge = CvBridge()


def vision():
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        image_pub = rospy.Publisher("/camera", Image, queue_size = 1)
        rospy.init_node("webcam",anonymous = False)
        #rate = rospy.Rate(10)
        
        #self.bridge = CvBridge()
        while not rospy.is_shutdown():
            ret, img = vid.read()
            #vid.set(5, 10)
            #vid.set(3, 1280)
            #vid.set(4, 720)
            if not ret:
                break
            #img = cv2.resize(img,(640,360),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
            img = img[0:480, 0:636]
            #cv2.imshow("Image",img)
            msg = bridge.cv2_to_imgmsg(img,"bgr8")
            
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            image_pub.publish(msg)
        # subscribed Topic
            if rospy.is_shutdown():
                vid.release()

def main():
    
    try:
        vision()
        #rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS Image feature detector module")
    cv2.destroyAllWindows()
    vid.release()

if __name__ == '__main__':
    main()
