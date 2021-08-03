from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import glob
import logging
import enum
import numpy as np
import functions.movement_detection as detection
import functions.video_utils as utils


class CameraState(enum.Enum):
    NO_MOVEMENT_DETECTED = 1
    DETECTING_MOVEMENT = 2
    DONE = 3


class CameraController():
    def __init__(self):
        self.__camera = None
        try:
            self.__camera = PiCamera()
            self.__camera.resolution = (600, 600)
            self.__camera.framerate = 20
            self.__camera.vflip = True
            # allow the camera to warmup
            time.sleep(0.1)
        except BaseException as e:
            logging.error(f"Could not connect to camera: {e}")

    def get_frames(self, nframes=10):
        if self.__camera:
            try:
                self.__camera.capture_sequence(
                    ['image%02d.jpg' % i for i in range(10)])
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

    def record_until_detect_movement(self, filename="output", timeout=120):
        raw_capture = PiRGBArray(self.__camera, size=self.__camera.resolution)
        state = CameraState.NO_MOVEMENT_DETECTED
        background_frame = None
        start_time = time.time()
        video_frames = []
        for frame in self.__camera.capture_continuous(
                raw_capture, format='bgr', use_video_port=True):
            raw_capture.truncate(0)
            img = np.array(frame.array)
            # detect movement
            if background_frame is None:
                background_frame = detection.grey_and_blur(img)

            else:
                if detection.frame_contains_movement(img, background_frame):
                    video_frames.append(img)
                    if len(video_frames) > 100:
                        state = CameraState.DONE
                else:
                    if len(video_frames) > 5:
                        state = CameraState.DONE
                    else:
                        # Not enough frames, start over
                        state = CameraState.NO_MOVEMENT_DETECTED
                        video_frames = []
                        background_frame = None
            if time.time() - start_time > timeout:
                logging.error("Timed out")
                return False

            if state == CameraState.DONE:
                logging.info(
                    f"Finished capturing - acquired {len(video_frames)} frames")
                utils.write_gif(filename, video_frames)
                return True
