
import cv2
import numpy as np
import functions.movement_detection as detect
cap = cv2.VideoCapture('video.mp4')
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

fc = 0
ret = True

while (fc < frameCount and ret):
    ret, buf[fc] = cap.read()
    fc += 1

cap.release()


detect.detect_movement(buf)
