#
#!/usr/bin/env python3
import rospy
import pyshine as ps
# OpenCV2 for saving an image
import cv2
# ROS Image message
import numpy as np
from sensor_msgs.msg import Image
import requests
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
import pickle
import struct
import socket
import imutils

HTML="""
<html>
<head>
<title>Mayavi Live Streaming</title>
</head>
<body>
<center><h1> Mayavi Live Streaming using OpenCV </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""

# Instantiate CvBridge
bridge = CvBridge()
address = ('192.168.235.108',9004)
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)
client_socket,addr=server_socket.accept()
def image_callback(msg):
    try:
        #StreamProps = ps.StreamProps
        #StreamProps.set_Page(StreamProps,HTML)
        #address = ('192.168.235.108', 9000) # Enter your IP address

        # Convert your ROS Image message to OpenCV2
        print("Received an image!")
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        a=pickle.dumps(cv2_img)
        message=struct.pack("Q",len(a))+a
        client_socket.sendall(message)
        #(rows,cols,channels) = cv2_img.shape
        #data=pickle.dumps(cv2_img)
        #cv2_img.set(cv2.CAP_PROP_BUFFERSIZE,4)
        #cv2_img.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        #cv2_img.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        #cv2_img.set(cv2.CAP_PROP_FPS,30)
        #cv2.imshow("sub",cv2_img)
        #StreamProps.set_Capture(StreamProps, cv2_img)
        #StreamProps.set_Quality(StreamProps, 90)
        #server = ps.Streamer(address,StreamProps)
        #print('Server started at','http://'+address[0]+':'+str(address[1]))
        #server.serve_forever()
    except CvBridgeError:
        print(CvBridgeError)
        #capture.release()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()
    else:
        cv2.imshow("sub",cv2_img)
        cv2.waitKey(10)
        #cv2.imwrite('camera_image.jpeg', cv2_img)

def main():
    rospy.init_node('image_listener')
    rospy.Subscriber("/camera" ,Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()

