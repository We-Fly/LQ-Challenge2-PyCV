import cv2
import numpy as np


capture = cv2.VideoCapture(0)                                                                                   # 读取视频

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
        cv2.putText(frame, text, (np.int32(rect[0][0]), np.int32(rect[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                   (0, 0, 255), 2)
        i += 1
    return image

while (True):
    ret, frame = capture.read()
    if ret is True:
        result = process(frame)
        cv2.imshow("result", result)
        c = cv2.waitKey(1)
    else:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
