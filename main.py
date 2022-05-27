import cv2
import numpy as np


cap=cv2.VideoCapture(0)
count=0

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
firstframe=None


ball_color = ['green', 'red', 'blue']


def process(image, opt=1):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                                                          # RGB转HSV色彩空间
    line = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15), (-1, -1))                                          # 结构元素

    mask_red = cv2.inRange(hsv, (0, 60, 60), (50, 255, 255))                                                     # HSV范围
    mask_blue = cv2.inRange(hsv, (100, 80, 46), (124, 255, 255))
    mask_green = cv2.inRange(hsv, (35, 43, 35), (90, 255, 255))
    mask_yellow = cv2.inRange(hsv, (11, 34, 43), (46, 255, 255))

    masks = [mask_red, mask_blue, mask_green, mask_yellow]


    i = 1                                                                                           # 轮廓提取, 发现最大轮廓
    for mask in masks:

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        index = -1
        max = 0
        for c in range(len(contours)):
            area = cv2.contourArea(contours[c])
            if area > max:
                max = area
                index = c
        # 绘制
        if index >= 0:
            rect = cv2.minAreaRect(contours[index])
            # 椭圆拟合
            cv2.ellipse(image, rect, (255, 0, 0), 2, 8)
            # 中心点定位
            cv2.circle(image, (np.int32(rect[0][0]), np.int32(rect[0][1])), 2, (0, 255, 0), 2, 8, 0)
        if i == 1:
            text = 'red'
        elif i == 2:
            text = 'blue'
        elif i == 3:
            text = 'green'
        elif i == 4:
            text = 'yellow'
        cv2.putText(image, text, (np.int32(rect[0][0]), np.int32(rect[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                   (0, 0, 255), 2)
        print(text)
        i += 1
    return image

def shapedetection(img):
    contours,hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    global x, y, w, h
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
    print(objType)
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
       final_img=process(final_img)
       cv2.imshow('final_img',final_img)
       key = cv2.waitKey(1)
    else:
        break
