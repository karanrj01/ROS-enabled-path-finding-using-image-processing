# import the opencv library
import cv2
import numpy as np


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

# define a video capture object
vid = cv2.VideoCapture(-1)

while(True):
	
    # Capture the video frame
    # by frame
    ret, img = vid.read()
    img = img[0:480, 0:620]

    # Display the resulting frame
    # cv2.imshow('frame', frame)
# --------------- here ---------------
    contours, hierarchy = cv2.findContours(preprocess(img), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
        hull = cv2.convexHull(approx, returnPoints=False)
        sides = len(hull)
        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
        #print(sides)
        print(img.shape)

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
                      elif(cx<arrow_tip[0]):
                            cv2.putText(img, "right", (cx - 20, cy - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                      if (cy>arrow_tip[1]):
                            cv2.putText(img, "up", (cx + 20, cy + 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                      elif(cy<arrow_tip[1]):
                            cv2.putText(img, "down", (cx + 20, cy + 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # --------------- here ---------------
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
