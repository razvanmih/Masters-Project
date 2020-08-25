import numpy as np

import Environment
from Agent import Agent

if __name__ == '__main__':
    action_space = [i for i in range(9)]


    Environment.init_environment()


    agent = Agent(gamma=0.99, epsilon=0, lr=1e-3, input_dims=[1,4, 300, 168],
                  eps_dec=1e-3, mem_size=10, batch_size=50, eps_min=0,
                  replace=50, n_actions=9)

    agent.load_models('2020-08-24_00-19')

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


            step_number += 1
            state = new_state
            processed_state = new_processed_state

            if step_number >= step_limit:
                break
