from pynput.keyboard import Key

up = {'w'}
down = {'s'}
left = {'a'}
right = {'d'}

up_and_right = up | right
up_and_left = up | left
down_and_right = down | right
down_and_left = down | left

stand = set()

one = '1'
two = '2'
three = '3'

enter = Key.enter

keys = [up, up_and_left, up_and_right,
        down, down_and_left, down_and_right,
        left, right,
        one, two, three,
        enter]


def get_key_by_value(key):
    for keyConst in keys:
        if keyConst == str(key):
            return keyConst
