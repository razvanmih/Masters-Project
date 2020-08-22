from pynput.keyboard import Controller
from Utils import InputConst
import random
import time

keyboard = Controller()

current_direction = set()


def clear_directional_input_except(kept_input=set()):
    clear_input = current_direction - kept_input
    for d in clear_input:
        current_direction.remove(d)
        keyboard.release(d)


def press_play():
    keyboard.press(InputConst.enter)
    keyboard.release(InputConst.enter)


def set_direction(new_direction=set()):
    clear_directional_input_except(new_direction)
    for direction in new_direction:
        if direction not in current_direction:
            current_direction.add(direction)
            keyboard.press(direction)


def take_action(action):
    action_mapping.get(action)()


def go_up():
    set_direction(InputConst.up)


def go_down():
    set_direction(InputConst.down)


def go_left():
    set_direction(InputConst.left)


def go_right():
    set_direction(InputConst.right)


def go_up_and_right():
    set_direction(InputConst.up_and_right)


def go_up_and_left():
    set_direction(InputConst.up_and_left)


def go_down_and_right():
    set_direction(InputConst.down_and_right)


def go_down_and_left():
    set_direction(InputConst.down_and_left)


def stand():
    set_direction(InputConst.stand)


action_mapping = {
    InputConst.stand: stand,
    InputConst.up: go_up,
    InputConst.down: go_down,
    InputConst.left: go_left,
    InputConst.right: go_right,
    InputConst.up_and_left: go_up_and_left,
    InputConst.up_and_right: go_up_and_right,
    InputConst.down_and_left: go_down_and_left,
    InputConst.down_and_right: go_down_and_right
}


def press_one():
    keyboard.press(InputConst.one)
    keyboard.release(InputConst.one)
    clear_input()


def press_two():
    keyboard.press(InputConst.two)
    keyboard.release(InputConst.two)
    clear_input()


def press_three():
    keyboard.press(InputConst.three)
    keyboard.release(InputConst.three)
    clear_input()


def press_key(key):
    keyboard.press(key)
    keyboard.release(key)
    clear_input()


def end_current_game():
    keyboard.press(InputConst.pause)
    keyboard.release(InputConst.pause)
    time.sleep(.15)
    keyboard.press(InputConst.home)
    keyboard.release(InputConst.home)
    time.sleep(.15)
    keyboard.press(InputConst.confirm)
    keyboard.release(InputConst.confirm)
    clear_input()


def game_over_script():
    time.sleep(.5)
    keyboard.press(InputConst.one)
    keyboard.release(InputConst.one)
    time.sleep(3)
    keyboard.press(InputConst.one)
    keyboard.release(InputConst.one)
    keyboard.press(InputConst.one)
    keyboard.release(InputConst.one)
    keyboard.press(InputConst.one)
    keyboard.release(InputConst.one)
    clear_input()


def clear_input():
    clear_directional_input_except()


def lvl_up_script():
    key = random.randint(1, 3)
    press_key(str(key))
    clear_input()
