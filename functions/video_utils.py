import cv2
from PIL import Image


def write_gif(filename_stem, frame_array):
    if len(frame_array) == 0:
        return False
    shape = frame_array[0].shape

    mode = 'RGB' if len(shape) == 3 else None
    filename_gif = filename_stem + ".gif"
    imgs = [Image.fromarray(img, mode) for img in frame_array]
    # duration is the number of milliseconds between frames; this is 40 frames
    # per second
    imgs[0].save(filename_gif, save_all=True,
                 append_images=imgs[1:], duration=50, loop=0)
    return True
