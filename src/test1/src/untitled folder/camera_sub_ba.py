#!/usr/bin/env python3
import rospy
# OpenCV2 for saving an image
import cv2
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError


# Instantiate CvBridge
bridge = CvBridge()

def image_callback(msg):
    
    try:
        # Convert your ROS Image message to OpenCV2
        print("Received an image!")
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imshow("sub",cv2_img)
    except CvBridgeError:
        print(CvBridgeError)
    else:
        cv2.imshow("sub",cv2_img)
        cv2.waitKey(10)
        #cv2.imwrite('camera_image.jpeg', cv2_img)

def main():
    rospy.init_node('image_listener')
    # Define your image topic
    
    # Set up your subscriber and define its callback
    rospy.Subscriber("/camera" ,Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()

