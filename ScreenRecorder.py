import d3dshot
import time
import cv2
from Utils.Exceptions import NoFrameCapturedException, FrameRateExceededException

d: d3dshot.D3DShot = None
timestamp = 0

def create(capture_output="numpy", frame_buffer_size=60,
           display=1,
           top: int = 40,
           left: int = 0,
           width: int = 562,
           height: int = 1000):
    global d
    d = d3dshot.create(capture_output, frame_buffer_size)
    d.display = d.displays[display]
    d.capture(region=(left, top, left + width, top + height))



def capture():
    d.capture()


def get_frame(frame_rate=30):
    global timestamp
    curr_time = time.time()
    if curr_time - timestamp < .97 / frame_rate:
        raise FrameRateExceededException()
    timestamp = curr_time
    frame = d.get_latest_frame()

    if frame is None:
        raise NoFrameCapturedException()

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame


def stop():
    d.stop()
