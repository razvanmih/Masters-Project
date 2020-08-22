import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


def equal_similarity(img1, img2):
    equal_eval = np.array(img1 == img2)
    return np.count_nonzero(equal_eval) / equal_eval.size


def hist_similarity(hist1, hist2):
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    # print(score)
    return score


def get_play_btn_area(frame):
    return np.copy(frame[705:815, 168:395])


def get_gameplay_check_area(frame):
    # return np.copy(frame[20:50, -120:-90])
    return np.copy(frame[27:42, -112:-97])


def get_lvl_up_text_image(frame):
    return np.copy(frame[165:235, 20:-20])


def get_death_screen_area(frame):
    return np.copy(frame[310:400, 50:-50])


def get_image_hist(image):
    color_hist = None
    for channel in range(3):
        hist = cv2.calcHist([image], [channel], None, [256], [0, 256])
        if color_hist is None:
            color_hist = np.copy(hist)
        else:
            color_hist = np.hstack((color_hist, hist))

    return color_hist


def plot_hist(hist):
    color = ('b', 'g', 'r')
    for channel, col in enumerate(color):
        histr = hist[:, channel]
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.title('Histogram for color scale picture')
    plt.show()


def get_hp_img(frame, hp_bar_template):
    img_blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hp_bar_region = np.copy(img_blur[370:485])

    res = cv2.matchTemplate(hp_bar_region, hp_bar_template, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = (max_loc[0], max_loc[1] + 370 - 15)
    bottom_right = (top_left[0] + 80, top_left[1] + 20)
    hp_bar_img = np.copy(frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]])

    return hp_bar_img


def process_hp_bar(hp_bar_img):
    hp_bar_img = cv2.resize(hp_bar_img, (0, 0), fx=5, fy=5)

    mask = cv2.inRange(hp_bar_img, (220, 220, 220), (255, 255, 255))
    hp_bar_img = cv2.bitwise_and(hp_bar_img, hp_bar_img, mask=mask)

    hp_bar_img = cv2.cvtColor(hp_bar_img, cv2.COLOR_BGR2GRAY)

    # hp_bar_img[hp_bar_img < 220] = 0
    # kernel = np.ones((2, 2), np.uint8)
    # hp_bar_img = cv2.morphologyEx(hp_bar_img, cv2.MORPH_DILATE, kernel)

    # hp_bar_img = cv2.resize(hp_bar_img, (0, 0), fx=2, fy=2)
    hp_bar_img = cv2.GaussianBlur(hp_bar_img, (3, 3), 0)
    hp_bar_img[hp_bar_img > 50] = 255

    kernel = np.ones((2, 2), np.uint8)
    hp_bar_img = cv2.dilate(hp_bar_img, kernel, 2)
    hp_bar_img = cv2.erode(hp_bar_img, kernel, 1)
    # hp_bar_img = cv2.dilate(hp_bar_img, kernel, 1)
    # hp_bar_img = cv2.morphologyEx(hp_bar_img, cv2.MORPH_DILATE, kernel)

    hp_bar_img = cv2.cvtColor(hp_bar_img, cv2.COLOR_GRAY2RGB)

    return hp_bar_img


def load_asset(path: str):
    return cv2.imread(path)


def save_asset(name: str, asset):
    cv2.imwrite('../Assets/' + name + '.png', asset)


def read_image(hp_img):
    return pytesseract.image_to_string(hp_img, config=' --psm 7')


def detect_enemy_hp_bars(frame):
    img_copy = frame.copy()
    debug_frame = frame.copy()

    mask = cv2.inRange(frame, (25, 55, 170), (60, 100, 250))
    # mask = cv2.inRange(img, (25, 55, 170), (60, 100, 250))
    # mask = cv2.inRange(img, (35, 75, 200), (50, 120, 245))
    img_copy = cv2.bitwise_and(img_copy, img_copy, mask=mask)

    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    img_copy[img_copy != 0] = 255

    # kernel = np.ones((5, 5), np.uint8)
    # img_copy = cv2.morphologyEx(img_copy, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((1, 14), np.uint8)
    img_copy = cv2.erode(img_copy, kernel, iterations=1)
    # kernel = np.ones((3, 3), np.uint8)
    # img_copy = cv2.dilate(img_copy, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(img_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
    # print(len(contours))
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # w = 67
        # h = 6
        cv2.rectangle(debug_frame, (x - 8, y - 5), (x + 60, y + 6), (255, 0, 100), 1)

    return contours, debug_frame


def get_hp_bar_from_cnt(cnt, frame):
    x, y, _, _ = cv2.boundingRect(cnt)
    x -= 7
    y -= 5
    w = 69
    h = 11

    if y < 0:
        return

    hp_bar = np.copy(frame[y:y + h, x:x + w])
    hp_bar = cv2.cvtColor(hp_bar, cv2.COLOR_BGR2GRAY)
    # if hp_bar.shape[0] == 11:
    return hp_bar


def get_exit_detection(frame):
    img_copy = frame.copy()
    debug_frame = frame.copy()

    mask = cv2.inRange(frame, (100, 254, 254), (250, 255, 255))  # blu 150
    img_copy = cv2.bitwise_and(img_copy, img_copy, mask=mask)

    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    img_copy[img_copy != 0] = 255
    kernel = np.ones((3, 3), np.uint8)
    img_copy = cv2.erode(img_copy, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(img_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 200]
    y_positions = [cv2.boundingRect(cnt)[1] for cnt in contours]

    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (255, 0, 100), 2)

    return y_positions


def debug(frame):
    img_copy = frame.copy()
    debug_frame = frame.copy()

    mask = cv2.inRange(frame, (100, 254, 254), (250, 255, 255))
    img_copy = cv2.bitwise_and(img_copy, img_copy, mask=mask)

    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    img_copy[img_copy != 0] = 255
    kernel = np.ones((4, 4), np.uint8)
    img_copy = cv2.erode(img_copy, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(img_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 200]
    y_positions = [cv2.boundingRect(cnt)[1] for cnt in contours]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (255, 0, 100), 2)

    return img_copy, debug_frame


def convert_color_to_gray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def show(frame, title='DEBUG_FRAME'):
    cv2.imshow(title, frame)


def process_frame_for_agent(frame):
    frame = frame.copy()
    frame = convert_color_to_gray(frame)
    frame = cv2.resize(frame, (0, 0), fx=.3, fy=.3)

    return frame
