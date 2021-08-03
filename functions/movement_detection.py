import numpy as np
import cv2


def grey_and_blur(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 9)
    return gray


def is_frame_relevant(contours):
    if len(contours) == 0:
        return False
    else:
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                return True
        return False


def frame_contains_movement(frame, background_frame):
    blurred_frame = grey_and_blur(frame)
    diff_frames = cv2.absdiff(background_frame, blurred_frame)
    _, thresh = cv2.threshold(diff_frames, 25, 255, cv2.THRESH_BINARY)
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return is_frame_relevant(contours)


def detect_movement(frame_sequence):
    if len(frame_sequence) == 0:
        return None
    first_frame = grey_and_blur(frame_sequence[0])
    for frame in frame_sequence[1:]:
        if frame_contains_movement(frame, first_frame):
            cv2.imshow("frame", frame)
            cv2.waitKey(33)
        first_frame = frame
