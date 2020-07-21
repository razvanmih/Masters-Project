import cv2
import time
from Utils.Exceptions import FrameRateExceededException, NoFrameCapturedException
import ScreenRecorder as sr
import ImageManager as im
import GameManager as gm
from Utils import Configuration as config

prvs_time = 0

sr.create()
play_btn = im.load_asset(config.play_btn_path)

while True:
    curr_time = time.time()

    try:
        frame = sr.get_frame(frame_rate=30)
    except FrameRateExceededException:
        continue
    except NoFrameCapturedException:
        continue

    # play_btn_area = im.get_play_btn_area(frame)
    # print(play_btn_area.shape, play_btn.shape)
    # print(im.equal_similarity(play_btn, play_btn_area))

    print(gm.is_in_menu(frame))

    cv2.imshow('test2', frame)
    # cv2.imshow('test2', play_btn_area)

    print('fps: {0}'.format(1 / (curr_time - prvs_time)))
    prvs_time = curr_time




    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
