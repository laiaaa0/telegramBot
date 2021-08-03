import unittest
import numpy as np
import functions.video_utils as video
from os import path


class TestVideoUtils(unittest.TestCase):
    def test_video_saver_3_channels(self):
        video_array = []
        for i in range(10):
            fake_array = np.zeros((100, 100, 3))
            fake_array.fill(i)
            video_array.append(fake_array)

        video_filename = "filename3"
        self.assertTrue(video.write_gif(video_filename, video_array))
        self.assertTrue(path.exists(video_filename + ".gif"))

    def test_video_saver_1_channel(self):
        video_array = []
        for i in range(10):
            fake_array = np.zeros((100, 100))
            fake_array.fill(i)
            video_array.append(fake_array)

        video_filename = "filename1"
        self.assertTrue(video.write_gif(video_filename, video_array))
        self.assertTrue(path.exists(video_filename + ".gif"))
