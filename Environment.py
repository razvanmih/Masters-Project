import os
from collections import deque
from Utils import InputConst, Configuration
import ImageManager
import GameManager
import GameController
from Utils import GameStateConst
import pygetwindow as gw
import pickle
from concurrent.futures import ThreadPoolExecutor

blue_stacks = gw.getWindowsWithTitle('BlueStacks')[0]
blue_stacks.activate()

action_space = [InputConst.up, InputConst.down,
                InputConst.left, InputConst.right,
                InputConst.up_and_left, InputConst.up_and_right,
                InputConst.down_and_left, InputConst.down_and_right,
                InputConst.stand]

current_state = deque(maxlen=5)
processed_state = deque(maxlen=5)

done = None
step_counter = None


def init_environment():
    GameManager.start_screen_recorder()


def close():
    GameManager.stop_screen_recorder()
    GameController.clear_input()


def set_done(value):
    global done
    done = value


def reset():
    global current_state, processed_state, done, step_counter
    current_state = deque(maxlen=5)
    processed_state = deque(maxlen=5)
    done = False
    step_counter = 0
    GameController.clear_input()

    game_state = GameStateConst.GAMEPLAY
    while game_state is GameStateConst.GAMEPLAY:
        frame = GameManager.get_frame(frame_rate=999)
        game_state = GameManager.get_current_state(frame)
        if game_state is GameStateConst.GAMEPLAY:
            GameController.end_current_game()

    while True:
        frame = GameManager.get_frame(frame_rate=999)
        game_state = GameManager.get_current_state(frame)
        if game_state is GameStateConst.GAMEPLAY:
            update_state(frame, False)

            return current_state, processed_state, done

        if game_state is GameStateConst.MENU_SCREEN:
            GameController.press_play()


def update_state(frame, new_done):
    set_done(new_done)
    current_state.append(frame)
    processed_frame = ImageManager.process_frame_for_agent(frame)
    processed_state.append(processed_frame)
    while len(current_state) < 5:
        current_state.append(frame)
        processed_state.append(processed_frame)

prev_state = 0
def step(action):
    global step_counter
    step_counter += 1
    GameController.take_action(action)

    while True:
        frame = GameManager.get_frame()
        game_state = GameManager.get_current_state(frame)

        # print("Current Frame:", step_counter, "Identified as:", game_state)

        if game_state is GameStateConst.UNDEF:
            GameController.clear_input()

        if game_state is GameStateConst.GAME_OVER_SCREEN:
            update_state(frame, True)
            GameController.game_over_script()
            return current_state, processed_state, done

        if game_state is GameStateConst.GAMEPLAY:
            update_state(frame, False)
            return current_state, processed_state, done

        if game_state is GameStateConst.LVL_TRANSITION_SCREEN:
            update_state(frame, False)
            GameController.clear_input()
            return current_state, processed_state, done

        if game_state is GameStateConst.LVL_UP_SCREEN:
            GameController.lvl_up_script()
        if game_state is GameStateConst.MENU_SCREEN:
            GameController.press_play()


def get_reward(state):
    reward = 0
    reward += get_exit_score(state[4], state[3])

    return reward


def get_exit_score(new_frame, old_frame):
    exit_score = GameManager.get_exit_score(new_frame) - GameManager.get_exit_score(old_frame)
    if abs(exit_score) > 10:
        exit_score = 0
    return exit_score


def save_state_data(reward, action, done_flag, time_stamp, game_number, step_number):
    save_path = Configuration.experience_batch_root_path + "Batch_" + str(time_stamp) + "/" \
                + "Game_" + str(game_number) + "/state_data/"
    file_name = "state_data_" + str(step_number) + ".pkl"
    try:
        os.makedirs(save_path)
    except FileExistsError:
        pass

    save_file = open(save_path + file_name, 'wb')
    pickle.dump((reward, action, done_flag), save_file)
    save_file.close()


def reward_state_and_save(state, action, done_flag, time_stamp, game_number, step_number):
    # print("I'm a thread saving the state data - " + str(step_number))
    save_state_data(get_reward(state), action, done_flag, time_stamp, game_number, step_number)


def save_frames(frame, processed_frame, time_stamp, game_number, step_number):
    # print("I'm a thread saving frames - " + str(step_number))
    frame_save_path = Configuration.experience_batch_root_path + "Batch_" + str(time_stamp) + "/" + \
                      "Game_" + str(game_number) + "/frames/"

    processed_save_path = Configuration.experience_batch_root_path + "Batch_" + str(time_stamp) + "/" + \
                          "Game_" + str(game_number) + "/processed_frames/"

    # save_frame(frame, "frame_" + str(step_number) + ".pkl", frame_save_path)
    save_frame(processed_frame, "processed_frame_" + str(step_number) + ".pkl", processed_save_path)


def save_frame(frame, file_name, save_path):
    try:
        os.makedirs(save_path)
    except FileExistsError:
        pass

    frame_file = open(save_path + file_name, 'wb')
    pickle.dump(frame, frame_file)
    frame_file.close()
