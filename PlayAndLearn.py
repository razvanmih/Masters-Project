import numpy as np
from collections import deque
from Agent import Agent
from Utils import InputConst, Configuration, CommonFunctions
import Environment
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
from datetime import datetime
import random

print("I am", __name__, "Starting up..")


def wait():
    return


def build_state_from_index(index, frames):
    ret = deque(maxlen=4)
    if index < 3:
        for i in range(4):
            ret.append(frames[0])
        for frame in frames[:index + 1]:
            ret.append(frame)
    else:
        for frame in frames[index - 3:index + 1]:
            ret.append(frame)

    return np.expand_dims(np.array(ret), axis=0)


def populate_memory(batch_time_stamp, game_number):
    game_path = Configuration.experience_batch_root_path + \
                Configuration.experience_batch_folder.format(batch_time_stamp) + \
                Configuration.game_folder.format(game_number)

    frames = CommonFunctions.get_files_from_path(game_path + Configuration.processed_frames_folder)
    frames = [CommonFunctions.get_frame_from_path(frame_path) for frame_path in frames]

    state_data = CommonFunctions.get_files_from_path(game_path + Configuration.state_data_folder)
    state_data_list = [CommonFunctions.get_state_data(file_path) for file_path in state_data]

    for index, state_data in enumerate(state_data_list):
        if state_data[1] is None:
            break
        _state = build_state_from_index(index, frames)
        _new_state = build_state_from_index(index + 1, frames)
        agent.memory.store_transition(_state, state_data[1], state_data[0], _new_state, state_data[2])


def init_memory(batch_time_stamp):
    for i in range(10):
        populate_memory(batch_time_stamp, i)


if __name__ == '__main__':
    action_space = [i for i in range(9)]

    Configuration.current_run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    Environment.init_environment()
    saveFrameThreadExecutor = ThreadPoolExecutor(max_workers=4)
    saveStateThreadExecutor = ThreadPoolExecutor(max_workers=4)
    futures = []

    agent = Agent(gamma=0.99, epsilon=1, lr=1e-3, input_dims=[1,4, 300, 168],
                  eps_dec=1e-3, mem_size=1000, batch_size=50, eps_min=.0001,
                  replace=50, n_actions=9)

    init_memory("2020-08-23_18-51")

    print("agent has preloaded", agent.memory.mem_cntr, "transitions.")

    game_limit = 1
    step_limit = 50

    for game_number in range(game_limit):
        print("Start Game Number:", game_number)
        step_number = 0
        state, processed_state, done = Environment.reset()
        while not done:

            # action = random.choice([InputConst.up, InputConst.up_and_left, InputConst.up_and_right])
            # action = random.choice(action_space)
            action = agent.choose_action(np.expand_dims(processed_state, axis=0))
            new_state, new_processed_state, done = Environment.step(action)


            futures.append(saveStateThreadExecutor.submit(
                Environment.reward_state_and_save, state.copy(), action, done,
                Configuration.current_run_timestamp, game_number, step_number))

            futures.append(saveFrameThreadExecutor.submit(
                Environment.save_frames, state[-1], processed_state[-1],
                Configuration.current_run_timestamp, game_number, step_number))

            step_number += 1
            state = new_state
            processed_state = new_processed_state

            if step_number >= step_limit:
                break

        saveStateThreadExecutor.submit(
            Environment.reward_state_and_save, state.copy(), None, done,
            Configuration.current_run_timestamp, game_number, step_number)
        saveFrameThreadExecutor.submit(
            Environment.save_frames, state[-1], processed_state[-1],
            Configuration.current_run_timestamp, game_number, step_number)

        while False in [future.done() for future in futures]:
            wait()
        print("End of game", game_number, 'at step', step_number)

        populate_memory(Configuration.current_run_timestamp, game_number)

        for i in range(100):
            print("Starting learn phase:",i,"/50")
            agent.learn()

    agent.save_models(Configuration.current_run_timestamp)

    Environment.close()
    saveFrameThreadExecutor.shutdown(wait=True)
    saveStateThreadExecutor.shutdown(wait=True)

# if __name__ == '__main__':
#
#     n_games = 400
#
#
#     scores, eps_history = [], []
#
#     for i in range(n_games):
#         done = False
#         score = 0
#         observation = Environment.reset()
#         while not done:
#             action = agent.choose_action(observation)
#             new_state, new_processed_state, done = Environment.step(action)
#
#             agent.store_transition(observation, action, reward, observation_, done)
#             observation = observation_
#
#         agent.learn()
#         eps_history.append(agent.epsilon)
#         scores.append(score)
#
#         avg_score = np.mean(scores[-100:])
#         print('episode ', i, 'score %.1f' % score,
#                 'average score %.1f' % avg_score,
#                 'epsilon %.2f' % agent.epsilon)
#
#
