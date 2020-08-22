import ImageManager as im
import numpy as np
from Utils import Configuration as config
from Utils import GameStateConst
from concurrent import futures
import multiprocessing
import ScreenRecorder
from Utils.Exceptions import FrameRateExceededException, NoFrameCapturedException

play_btn_asset = im.load_asset(config.play_btn_path)
hp_bar_template = im.load_asset(config.hp_bar_path)

lvl_up_text_image_template = im.load_asset(config.lvl_up_text_image_path)
lvl_up_template_hist = im.get_image_hist(lvl_up_text_image_template)

death_message_asset = im.load_asset(config.death_message_path)
death_message_asset_hist = im.get_image_hist(death_message_asset)

gameplay_check_asset = im.load_asset(config.gameplay_check_asset_path)
gameplay_check_asset_hist = im.get_image_hist(gameplay_check_asset)


def start_screen_recorder():
    ScreenRecorder.create()


def stop_screen_recorder():
    ScreenRecorder.stop()


def is_in_menu(frame):
    play_btn_area = im.get_play_btn_area(frame)

    if im.equal_similarity(play_btn_area, play_btn_asset) > .8:
        return True
    return False


def is_level_up_screen(frame):
    lvl_up_text_image = im.get_lvl_up_text_image(frame)
    lvl_up_hist = im.get_image_hist(lvl_up_text_image)

    if im.hist_similarity(lvl_up_hist, lvl_up_template_hist) >= .9:
        return True
    return False


def is_game_over_screen(frame):
    death_message = im.get_death_screen_area(frame)
    death_message_hist = im.get_image_hist(death_message)

    if im.hist_similarity(death_message_hist, death_message_asset_hist) >= .9:
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


def is_lvl_transition_screen(frame):
    gray_frame = im.convert_color_to_gray(frame)
    frame_avg = np.average(gray_frame)
    if frame_avg < 30:
        return True
    return False


def is_gameplay_screen(frame):
    gameplay_check = im.get_gameplay_check_area(frame)
    gameplay_check_hist = im.get_image_hist(gameplay_check)

    # print(im.hist_similarity(gameplay_check_hist, gameplay_check_asset_hist))

    if im.hist_similarity(gameplay_check_hist, gameplay_check_asset_hist) >= .93:
        return True

    return False


def is_boss_battle_screen(frame):
    return False


def is_angel_screen(frame):
    return False


def is_lucky_wheel_screen(frame):
    return False


def is_devil_screen(frame):
    return False


state_checker_mapping = {
    # BOSS_BATTLE /is_boss_battle_screen not included
    # this will be checked for in cas of gameplay state as it is a subtype of gameplay

    GameStateConst.GAMEPLAY: is_gameplay_screen,
    GameStateConst.MENU_SCREEN: is_in_menu,
    GameStateConst.GAME_OVER_SCREEN: is_game_over_screen,
    GameStateConst.LVL_UP_SCREEN: is_level_up_screen,
    GameStateConst.ANGEL_SCREEN: is_angel_screen,
    GameStateConst.LUCKY_WHEEL_SCREEN: is_lucky_wheel_screen,
    GameStateConst.DEVIL_SCREEN: is_devil_screen,
    GameStateConst.LVL_TRANSITION_SCREEN: is_lvl_transition_screen
}


def get_current_state(frame):
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_checker_state_mapping = dict()
        for game_state in state_checker_mapping.keys():
            future_checker = executor.submit(state_checker_mapping.get(game_state), frame)
            future_checker_state_mapping[future_checker] = game_state

        for checker in future_checker_state_mapping.keys():
            if checker.result():
                return future_checker_state_mapping.get(checker)

    return GameStateConst.UNDEF


def get_frame(frame_rate=30):
    frame = None
    while frame is None:
        try:
            frame = ScreenRecorder.get_frame(frame_rate=frame_rate)
        except FrameRateExceededException:
            continue
        except NoFrameCapturedException:
            continue
    return frame


def get_exit_score(frame):
    positions = im.get_exit_detection(frame)
    if len(positions):
        return np.ceil(min(positions)/10)
    return 0

