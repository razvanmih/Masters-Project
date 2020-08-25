import os
import pickle

def get_files_from_path(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    files.sort(key=get_file_index)
    return files

def get_file_index(file_path):
    index = file_path[-6:-4]
    if index.isnumeric():
        return int(index)
    else:
        return int(file_path[-5:-4])


def get_frame_from_path(file_path):
    with open(file_path, 'rb') as file:
        frame = pickle.load(file)

    return frame

def get_state_data(file_path):
    with open(file_path, 'rb') as file:
        reward, action, done_flag = pickle.load(file)

    return reward, action, done_flag