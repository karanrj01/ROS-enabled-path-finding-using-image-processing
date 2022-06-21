#!/usr/bin/env python3

# Python libs
#import sys, time

# numpy and scipy
import numpy as np
from std_msgs.msg import String
# OpenCV
import cv2
from cv_bridge import CvBridge, CvBridgeError 
# Ros libraries
import rospy

# Ros Messages
from sensor_msgs.msg import Image
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

#VERBOSE=False
vid = cv2.VideoCapture(0, cv2.CAP_V4L)
bridge = CvBridge()

def preprocess(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 50, 50)
    kernel = np.ones((3, 3))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode

def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 2
        if j > length - 1:
            j = length - j
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])


def vision():
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        left = 0
        right = 0
        arrow = ""
        image_pub = rospy.Publisher("/camera", Image, queue_size = 1)
        arrow_pub = rospy.Publisher("/arrow", String, queue_size = 10)
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
            contours, hierarchy = cv2.findContours(preprocess(img), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
                hull = cv2.convexHull(approx, returnPoints=False)
                sides = len(hull)
                cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                #print(sides)
                #print(img.shape)

                if 6 > sides > 3 and sides + 2 == len(approx):
                    arrow_tip = find_tip(approx[:,0,:], hull.squeeze())
                    if arrow_tip:
                        #cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                        cv2.circle(img, arrow_tip, 3, (0, 0, 255), cv2.FILLED)
                        M = cv2.moments(cnt)
                        if M['m00'] != 0:
                              cx = int(M['m10']/M['m00'])
                              cy = int(M['m01']/M['m00'])
                              cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                              if (cx>arrow_tip[0]):
                                    cv2.putText(img, "left", (cx - 20, cy - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                                    left += 1
                              elif(cx<arrow_tip[0]):
                                    cv2.putText(img, "right", (cx - 20, cy - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                                    right += 1
                              if (cy>arrow_tip[1]):
                                    cv2.putText(img, "up", (cx + 20, cy + 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                              elif(cy<arrow_tip[1]):
                                    cv2.putText(img, "down", (cx + 20, cy + 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            msg = bridge.cv2_to_imgmsg(img,"bgr8")
            if left > right:
                arrow = 'left'
            elif right > left:
                arrow = 'right'
            #cv2.imshow("Image",img)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            image_pub.publish(msg)
            arrow_pub.publish(arrow)
            #print(arrow)
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
