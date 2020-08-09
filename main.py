import cv2
import time
import pyautogui
from Utils.Exceptions import FrameRateExceededException, NoFrameCapturedException
from Utils import InputConst
import ScreenRecorder as sr
import ImageManager as im
import GameManager
from GameController import GameController
from Utils import Configuration as config
import pygetwindow as gw
from pynput.keyboard import Key, Controller
import numpy as np
import random

prvs_time = 0

pyautogui.FAILSAFE = True

sr.create()
gameController = GameController()
play_btn = im.load_asset(config.play_btn_path)

# print(gw.getAllTitles())

blue_stacks = gw.getWindowsWithTitle('BlueStacks')[0]
blue_stacks.activate()

keyboard = Controller()

t = time.time()
keyboard.press('a')
print(1 / (time.time() - t))
keyboard.release('a')

frame_counter = 30


def check_white(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_avg = np.average(gray_frame)
    if frame_avg > 230:
        return True
    return False


while True:
    curr_time = time.time()

    try:
        frame = sr.get_frame(frame_rate=30)
    except FrameRateExceededException:
        continue
    except NoFrameCapturedException:
        continue

    play_btn_area = im.get_play_btn_area(frame)
    lvl_up_text_image = im.get_lvl_up_text_image(frame)
    # cv2.imwrite("../Assets/lvl_up_text_image.png", lvl_up_text_image)
    # hist = im.get_image_hist(lvl_up_text_image)
    # im.plot_hist(hist)

    if GameManager.is_level_up_screen(frame):
        key = random.randint(1, 3)
        gameController.press_key(str(key))

    # cv2.imwrite("../Assets/play_btn.png",play_btn_area)
    # print(play_btn_area.shape, play_btn.shape)
    # print(im.equal_similarity(play_btn, play_btn_area))

    if check_white(frame):
        print("WHITE SCREEN")

    if GameManager.is_in_menu(frame):
        gameController.press_play()
    #
    # if frame_counter % 30 == 0:
    #     gameController.random_direction()

    hp_bars, debug_frame = GameManager.get_enemy_hp_bars(frame)

    # hp, hp_img = GameManager.get_current_hp(frame)
    #
    # hp_img = cv2.putText(hp_img, hp, (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('test', debug_frame)
    cv2.imshow('test1', lvl_up_text_image)
    if len(hp_bars) > 0:
        print(GameManager.count_hits(hp_bars))
        cv2.imshow('test2', hp_bars[0])


    # print('fps: {0}'.format(1 / (curr_time - prvs_time)))

    prvs_time = curr_time
    frame_counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
