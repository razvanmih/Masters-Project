from pynput.keyboard import Controller
from Utils import InputConst
import random


class GameController:

    def __init__(self):
        self.keyboard = Controller()

        self.current_direction = set()

    def clear_directional_input_except(self, kept_input=set()):
        clear_input = self.current_direction - kept_input
        for d in clear_input:
            self.current_direction.remove(d)
            self.keyboard.release(d)

    def press_play(self):
        self.keyboard.press(InputConst.enter)
        self.keyboard.release(InputConst.enter)

    def set_direction(self, new_direction=set()):
        self.clear_directional_input_except(new_direction)
        for direction in new_direction:
            if direction not in self.current_direction:
                self.current_direction.add(direction)
                self.keyboard.press(direction)

    def go_up(self):
        self.set_direction(InputConst.up)

    def go_down(self):
        self.set_direction(InputConst.down)

    def go_left(self):
        self.set_direction(InputConst.left)

    def go_right(self):
        self.set_direction(InputConst.right)

    def go_up_and_right(self):
        self.set_direction(InputConst.up_and_right)

    def go_up_and_left(self):
        self.set_direction(InputConst.up_and_left)

    def go_down_and_right(self):
        self.set_direction(InputConst.down_and_right)

    def go_down_and_left(self):
        self.set_direction(InputConst.down_and_left)

    def stand(self):
        self.set_direction(InputConst.stand)

    def random_direction(self):
        r = random.random()
        if r < .12:
            self.go_down()
            return
        if r < .23:
            self.go_down_and_right()
            return
        if r < .34:
            self.go_down_and_left()
            return
        if r < .45:
            self.go_up()
            return
        if r < .56:
            self.go_up_and_right()
            return
        if r < .67:
            self.go_up_and_left()
            return
        if r < .78:
            self.go_left()
            return
        if r < .89:
            self.go_right()
            return

        self.stand()

    def press_one(self):
        self.keyboard.press(InputConst.one)
        self.keyboard.release(InputConst.one)

    def press_two(self):
        self.keyboard.press(InputConst.two)
        self.keyboard.release(InputConst.two)

    def press_three(self):
        self.keyboard.press(InputConst.three)
        self.keyboard.release(InputConst.three)

    def press_key(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)
