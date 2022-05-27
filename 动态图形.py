import cv2
import numpy as np

cap=cv2.VideoCapture(0)
count=0

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
firstframe=None

def shapedetection(img):
    contours,hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for obj in contours:
        area = cv2.contourArea(obj)
        cv2.drawContours(img, obj, -1, (255, 0, 0), 4)
        perimeter = cv2.arcLength(obj,True)
        approx = cv2.approxPolyDP(obj,0.02*perimeter,True)
        CornerNum = len(approx)
        x, y, w, h = cv2.boundingRect(approx)

        if CornerNum ==3: objType ="triangle"
        elif CornerNum == 4:
            if w==h: objType= "Square"
            else:objType="Rectangle"
        elif CornerNum>4: objType= "Circle"
        else:objType="N"

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.putText(img,objType,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)
    return contours

while (True):
    ret,img=cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray=cv2.Canny(gray,60,60)
    if firstframe is None:
            firstframe = gray
            continue

    diff = cv2.absdiff(firstframe, gray)
    diff = cv2.threshold(diff, 148, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)

    if ret is True:
       final_img=shapedetection(img)
       cv2.imshow('final_img',final_img)
       key = cv2.waitKey(1)
    else:
        break

cap.release()
cv2.destroyAllWindows()