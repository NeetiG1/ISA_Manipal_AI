import numpy as np
import cv2

cap=cv2.VideoCapture(0)
while(True):
    ret,frame=cap.read()
    output=frame.copy()
    #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #converting to hsv and adding mask
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_blue=np.array([110,50,50])
    upper_blue=np.array([130,255,255])
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    mask=cv2.medianBlur(mask,5)



    #Creating Hough Circles
    circles=cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,255 ,param1=255 , param2=20,  minRadius=0, maxRadius=0)
    if circles is not None:
        detected_circles=np.uint16(np.around(circles))

        for (x,y,r) in detected_circles[0,:]:
            cv2.circle(output,(x,y),r,(0,0,255),2)
            print("detected ball")

    cv2.imshow('Output', output)


    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()