from mss import mss
import numpy as np
import time
from Utils.Exceptions import FrameRateExceededException


class ImageGrabber:
    def __init__(self, monitor: int = 1,
                 top: int = 40,
                 left: int = 0,
                 width: int = 562,
                 height: int = 1000):
        self.sct = mss()
        mon = self.sct.monitors[monitor]

        self.box = {'top': mon['top'] + top,
                    'left': mon['left'] + left,
                    'width': width,
                    'height': height}
        self.timestamp = 0

    def grab_screenshot(self, frame_rate: int = 30):
        curr_time = time.time()
        if curr_time - self.timestamp < .99/frame_rate:
            raise FrameRateExceededException()
        self.timestamp = curr_time
        return np.array(np.array(self.sct.grab(self.box))[:, :, :3])




    def close(self):
        self.sct.close()
