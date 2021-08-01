from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import glob
import logging
import enum
import np





class CameraController():
    def __init__(self):
        self.__camera = None
        try:
            self.__camera = PiCamera()
            self.__camera.resolution = (600,600)
            self.__camera.framerate = 20
            # allow the camera to warmup
            time.sleep(0.1)
        except BaseException as e:
            logging.error(f"Could not connect to camera: {e}")

    def get_frames(self, nframes=10):
        if self.__camera:
            try:
                self.__camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])
                return True
            except BaseException as e:
                logging.error(f"Could not capture sequence: {e}")
        else:
            logging.error("Requested frames but camera was not initialised")
        return False


    def cleanup(self):
        try:
            for filename in glob.glob("*.jpg"):
                os.remove(filename)
        except BaseException as e:
            logging.error("Failed to remove file")
            

    def record_until_detect_movement(self):
        raw_capture = PiRGBArray(self.__camera, size= self.__camera.resolution)
        state = NO_MOVEMENT_DETECTED
        for frame in self.__camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
            raw_capture.truncate(0)
            img = np.array(frame.array)
            # detect movement


