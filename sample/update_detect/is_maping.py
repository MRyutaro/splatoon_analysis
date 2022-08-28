import cv2
import numpy as np
import toml
import json
import time


def main():
    movie = cv2.VideoCapture(capture_mode_setting())
    open_position = open('config/json/position.json', 'r')
    position = json.load(open_position)
    frame_width, frame_height = position["frame_size"]["width"], position["frame_size"]["height"]

    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))

        # is_gaming = check_is_gaming(frame)
        # print(is_gaming)
        is_maping = check_is_maping(frame)
        print(is_maping)
        # ↓この範囲で画像認識させる
        cv2.rectangle(frame, (40, 25), (73, 60), (255, 0, 0), 1)
        # cv2.rectangle(frame, (300, 374), (465, 404), (255, 0, 0), 1)
        cv2.imshow('frame', cv2.resize(frame, (960, 540)))
        if cv2.waitKey(1) == 27:
            exit()
        time.sleep(0.1)


def capture_mode_setting():
    obj = toml.load("config/settings.toml")
    select_mode = obj["setting"]["MODE"]
    capture_content = 1
    if select_mode == "recorded":
        capture_content = obj["setting"]["VIDEO_PATH"]
    elif select_mode == "live":
        capture_content = obj["setting"]["PORT_NUM"]
    else:
        print("ERROR at settings.toml.")
        exit()
    return capture_content


def check_is_maping(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY)

    # x_icon = binary[35:55, 45:65]
    # # cv2.imshow('x_icon', cv2.resize(x_icon, (300, 300)))
    # # if cv2.waitKey(1) == 27:
    # #     exit()
    # unique, counts = np.unique(x_icon, return_counts=True)
    # result_x_icon = np.column_stack((unique, counts))
    # if len(result_x_icon) > 1:
    #     if result_x_icon[0][1] < 125 or result_x_icon[0][1] > 145:
    #         return False
    #     if result_x_icon[1][1] < 255 or result_x_icon[1][1] > 275:
    #         return False

    # down_button_icon = binary[374:404, 300:465]
    # unique, counts = np.unique(down_button_icon, return_counts=True)
    # result_down_button_icon = np.column_stack((unique, counts))
    # if len(result_down_button_icon) > 1:
    #     if result_down_button_icon[0][1] < 3300 or result_down_button_icon[0][1] > 2450:
    #         return False
    #     if result_down_button_icon[1][1] < 1450 or result_down_button_icon[1][1] > 1650:
    #         return False
    return True


if __name__ == "__main__":
    main()
