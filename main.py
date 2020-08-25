import cv2
import time
import pyautogui

import ImageManager
from Utils.Exceptions import FrameRateExceededException, NoFrameCapturedException
from Utils import InputConst, Configuration
import ScreenRecorder
import ImageManager as im
import GameManager
import GameController
import Environment
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Process
from Utils import Configuration as config
from Utils import GameStateConst

from pynput.keyboard import Key, Controller
import numpy as np
from datetime import datetime
import random

print("I am", __name__, "Starting up..")
if __name__ == '__main__':
    action_space = [i for i in range(9)]

    Configuration.current_run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    Environment.init_environment()
    saveFrameThreadExecutor = ThreadPoolExecutor(max_workers=4)
    saveStateThreadExecutor = ThreadPoolExecutor(max_workers=4)

    total_score = 0
    state, processed_state, done = Environment.reset()

    save_threads = []

    while not done:
        # if frame_counter > 10:
        #     avg_frame_rate = frame_counter / (time.time() - timer)
        #     print("avg frame rate", avg_frame_rate)
        # frame_counter += 1

        # action = random.choice([InputConst.up, InputConst.up_and_left, InputConst.up_and_right])
        # action = random.choice(action_space)
        action = 8 #InputConst.stand
        # action = 0 #InputConst.up
        new_state, new_processed_state, done = Environment.step(action)

        step_number = Environment.step_counter - 1

        # ImageManager.process_state_for_agent()

        frame = new_processed_state[4]

        state = new_state
        processed_state = new_processed_state
        # hp_bars, debug_frame = GameManager.get_enemy_hp_bars(frame)

        # hp, hp_img = GameManager.get_current_hp(frame)
        #
        # hp_img = cv2.putText(hp_img, hp, (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # frame = cv2.resize(frame, (0, 0), fx=.25, fy=.25)
        # frame = ImageManager.convert_color_to_gray(frame)

        # mask, debug_frame = ImageManager.debug(frame)
        #
        # cv2.imshow('test', mask)
        # cv2.imshow('debug_frame', frame)
        # # print(frame.shape)
        #
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
        #
        # if Environment.step_counter == 50:
        #     break

    Environment.close()

    saveFrameThreadExecutor.shutdown(wait=True)
    saveStateThreadExecutor.shutdown(wait=True)
