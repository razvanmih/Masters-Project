import cv2
import numpy as np


def equal_similarity(img1, img2):
    equal_eval = np.array(img1 == img2)

    return np.count_nonzero(equal_eval) / equal_eval.size


def get_play_btn_area(frame):
    return np.copy(frame[705:815, 168:395])


def load_asset(path: str):
    return cv2.imread(path)


def save_asset(name: str, asset):
    cv2.imwrite('../Assets/' + name + '.png', asset)
