import cv2
import numpy as np


cap = cv2.VideoCapture(0);


while(True):
    ret,frame = cap.read()
    #changing the frame to hsv
    hsvn = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #setting limits for bright red mask
    brightred_low = (0, 100, 100)
    brightred_high = (10, 255, 255)
    bright_red_mask = cv2.inRange(hsvn, brightred_low, brightred_high)
    #limits for dark red mask
    darkred_low = (160, 100, 100)
    darkred_high = (179, 255, 255)
    dark_red_mask = cv2.inRange(hsvn, darkred_low, darkred_high)
    #combining bright red and dark red
    weighted_mask = cv2.addWeighted(bright_red_mask, 1.0, dark_red_mask, 1.0, 0.0)

    blurred_mask = cv2.GaussianBlur(weighted_mask, (9, 9), 3, 3)

    erode = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    eroded_mask = cv2.erode(blurred_mask, erode)
    dilated_mask = cv2.dilate(eroded_mask, dilate)

    #detecting if a circle is present in the frame
    found = cv2.HoughCircles(dilated_mask, cv2.HOUGH_GRADIENT, 1, 150, param1=100, param2=50, minRadius=20,
                                        maxRadius=200)
    if found is not None:
        for circle in found[0, :]:
            circlepresent = cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), thickness=3)
        cv2.imshow("original", circlepresent)
        print("ball found")
    else:
        cv2.imshow("original", frame)
        print("no ball found")

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
