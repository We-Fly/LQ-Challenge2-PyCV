import cv2
import argparse

import imutils

from src.shapedetect import Picture, putChineseText

ap = argparse.ArgumentParser(
    prog="Little-Quadcopter",
    description="""
###################################################################################
   __ _ _   _   _              ____                 _                 _            
  / /(_) |_| |_| | ___        /___ \_   _  __ _  __| | ___ ___  _ __ | |_ ___ _ __ 
 / / | | __| __| |/ _ \_____ //  / / | | |/ _` |/ _` |/ __/ _ \| '_ \| __/ _ \ '__|
/ /__| | |_| |_| |  __/_____/ \_/ /| |_| | (_| | (_| | (_| (_) | |_) | ||  __/ |   
\____/_|\__|\__|_|\___|     \___,_\ \__,_|\__,_|\__,_|\___\___/| .__/ \__\___|_|   
                                                               |_|                 
###################################################################################
""",
    formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument("-i", "--image", help="path to the input image", type=str)

ap.add_argument("-w", "--webcam", help="start the webcam", type=int)

args = vars(ap.parse_args())


def image_opt() -> None:  # 图片操作
    image.drawShape(resize=500)
    cv2.imshow("image", image.resized)
    cv2.waitKey(0)


def frame_opt() -> None:  # 视频操作
    while 1:
        frame = Picture(webcam.read()[1])
        frame.drawShape(resize=300)
        cv2.imshow("capture", frame.resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if args["image"] is not None:  # 处理图片操作
    image = Picture(args["image"])
    image_opt()
elif args["webcam"] is not None:  # 处理视频操作
    webcam = cv2.VideoCapture(args["webcam"])
    frame_opt()
