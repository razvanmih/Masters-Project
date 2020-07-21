import ImageManager as im
from Utils import Configuration as config
from Utils import GameStateConst

play_btn_asset = im.load_asset(config.play_btn_path)


def is_in_menu(frame):
    play_btn_area = im.get_play_btn_area(frame)

    if im.equal_similarity(play_btn_area, play_btn_asset) > .95:
        return True
    return False

