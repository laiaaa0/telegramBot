import numpy as np
import cv2 

def greyAndBlur(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 9)
    return gray
    
def isFrameRelevant(contours):
    if len(contours) == 0 :
        return False
    else:
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                return True
        return False


def detect_movement(frame_sequence):
    if len(frame_sequence) == 0:
        return None
    first_frame = greyAndBlur(frame_sequence[0])
    for frame in frame_sequence[1:]:
        casted_frame = greyAndBlur(frame)
        diff_frames = cv2.absdiff(first_frame,casted_frame)
        _, thresh = cv2.threshold(diff_frames, 25, 255, cv2.THRESH_BINARY)
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        first_frame = casted_frame

        if isFrameRelevant(contours):
            cv2.imshow("diff", frame)
            cv2.waitKey(33)


