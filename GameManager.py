import ImageManager as im
import numpy as np
from Utils import Configuration as config
from Utils import GameStateConst

play_btn_asset = im.load_asset(config.play_btn_path)
hp_bar_template = im.load_asset(config.hp_bar_path)
lvl_up_text_image_template = im.load_asset(config.lvl_up_text_image_path)
lvl_up_template_hist = im.get_image_hist(lvl_up_text_image_template)


def is_in_menu(frame):
    play_btn_area = im.get_play_btn_area(frame)

    if im.equal_similarity(play_btn_area, play_btn_asset) > .90:
        return True
    return False


def is_level_up_screen(frame):
    lvl_up_text_image = im.get_lvl_up_text_image(frame)
    lvl_up_hist = im.get_image_hist(lvl_up_text_image)

    if im.hist_similarity(lvl_up_hist,lvl_up_template_hist) >= .9:
        return True
    return False




def get_current_hp(frame):
    hp_img = im.get_hp_img(frame, hp_bar_template)
    hp_img = im.process_hp_bar(hp_img)

    hp_value = im.read_image(hp_img)

    return hp_value, hp_img


def get_enemy_hp_bars(frame):
    hp_bar_cnts, debug_frame = im.detect_enemy_hp_bars(frame)
    hp_bars = [im.get_hp_bar_from_cnt(cnt, frame) for cnt in hp_bar_cnts]
    hp_bars = [hp_bar for hp_bar in hp_bars if hp_bar is not None]

    return hp_bars, debug_frame


def has_hit(hp_bar):
    return np.any(hp_bar > 250)


def count_hits(hp_bars):
    return np.sum([has_hit(hp_bar) for hp_bar in hp_bars])
