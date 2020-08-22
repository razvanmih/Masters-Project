from pynput.keyboard import Key

up = frozenset({'w'})
down = frozenset({'s'})
left = frozenset({'a'})
right = frozenset({'d'})

up_and_right = frozenset(up | right)
up_and_left = frozenset(up | left)
down_and_right = frozenset(down | right)
down_and_left = frozenset(down | left)

stand = frozenset()

one = '1'
two = '2'
three = '3'

enter = Key.enter

pause = 'p'
home = 'h'
confirm = '.'
cancel = ','

keys = [up, up_and_left, up_and_right,
        down, down_and_left, down_and_right,
        left, right,
        one, two, three,
        enter]


def get_key_by_value(key):
    for keyConst in keys:
        if keyConst == str(key):
            return keyConst
