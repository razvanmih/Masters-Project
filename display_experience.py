import os
import pickle
import cv2

game_path = "C:/Users/razva/OneDrive/Desktop/Folder/Disertatie/Main Project/Experience Batches/" \
            "Batch_2020-08-20_20-49/Game_1"
processed_frames = "/processed_frames"
frames = "/frames"
state_data_list = "/state_data"


def get_files_from_path(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def replay_frames(frames, state_data):
    for index, f in enumerate(frames):
        with open(f, 'rb') as file:
            frame = pickle.load(file)

        cv2.imshow('frame', frame)
        print(state_data[index])

        if state_data[index][0] == -5:
            cv2.waitKey(2000)

        if cv2.waitKey(40) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def get_state_data(f):
        with open(f, 'rb') as file:
            reward, action, done_flag = pickle.load(file)

        return reward, action, done_flag


processed_frames = get_files_from_path(game_path + processed_frames)
frames = get_files_from_path(game_path + frames)
state_data_list = get_files_from_path(game_path + state_data_list)

processed_frames.sort(key=os.path.getctime)
frames.sort(key=os.path.getctime)
state_data_list.sort(key=os.path.getctime)

# for f in processed_frames:
#     print(f, os.path.getctime(f))

print(len(processed_frames) / (max([os.path.getctime(f) for f in processed_frames]) - min(
    [os.path.getctime(f) for f in processed_frames])))

replay_frames(processed_frames,[get_state_data(state) for state in state_data_list])
# show_state_data(state_data_list)
# replay_frames(frames)
