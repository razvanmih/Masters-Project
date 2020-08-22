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
    action_space = [InputConst.up, InputConst.down,
                    InputConst.left, InputConst.right,
                    InputConst.up_and_left, InputConst.up_and_right,
                    InputConst.down_and_left, InputConst.down_and_right,
                    InputConst.stand]

    Configuration.current_run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    Environment.init_environment()
    saveFrameThreadExecutor = ThreadPoolExecutor(max_workers=4)
    saveStateThreadExecutor = ThreadPoolExecutor(max_workers=4)

    game_limit = 10
    step_limit = 200

    for game_number in range(game_limit):
        print("Start Game Number:", game_number)
        step_number = 0
        state, processed_state, done = Environment.reset()
        while not done:

            action = random.choice([InputConst.up, InputConst.up_and_left, InputConst.up_and_right])
            # action = random.choice(action_space)
            # action = InputConst.stand
            new_state, new_processed_state, done = Environment.step(action)

            frame = new_processed_state[4]

            saveStateThreadExecutor.submit(
                Environment.reward_state_and_save, state.copy(), action, done,
                Configuration.current_run_timestamp, game_number, step_number)

            saveFrameThreadExecutor.submit(
                Environment.save_frames, state[4], processed_state[4],
                Configuration.current_run_timestamp, game_number, step_number)

            step_number += 1
            state = new_state
            processed_state = new_processed_state

            if step_number >= step_limit:
                break

        saveStateThreadExecutor.submit(
            Environment.reward_state_and_save, state.copy(), None, done,
            Configuration.current_run_timestamp, game_number, step_number)
        saveFrameThreadExecutor.submit(
            Environment.save_frames, state[4], processed_state[4],
            Configuration.current_run_timestamp, game_number, step_number)

        time.sleep(1)

    Environment.close()
    saveFrameThreadExecutor.shutdown(wait=True)
    saveStateThreadExecutor.shutdown(wait=True)
