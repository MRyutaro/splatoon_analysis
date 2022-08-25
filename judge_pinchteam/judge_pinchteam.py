import cv2
import time
import json
import numpy as np


def setup_checkpoints(state_ranges):
    band = json.load(position)["band"]
    state_names = ["default", "friend_pinch", "enemy_pinch"]
    state_ranges = list()
    for state_name in state_names:
        tmp = band[state_name]
        state_ranges.append([[list(tmp["friend"]["min"].values()),
                            list(tmp["friend"]["max"].values())],
                             [list(tmp["enemy"]["min"].values()),
                            list(tmp["enemy"]["max"].values())]])

    checkpoints = list()
    for state in range(len(state_ranges)):
        checkpoints_by_state = list()
        for team in range(len(state_ranges[state])):
            width = state_ranges[state][team][1][0] - \
                state_ranges[state][team][0][0]
            height = state_ranges[state][team][1][1] - \
                state_ranges[state][team][0][1]
            # ここで点の位置を変える-------------------------------------
            for i in range(3):
                each_checkpoints = list()
                each_checkpoints.append(
                    int(state_ranges[state][team][0][0] + width*(i+1)/4))
                each_checkpoints.append(
                    int(state_ranges[state][team][0][1] + height/2))
            # ---------------------------------------------------------------
                checkpoints_by_state.append(each_checkpoints)
        checkpoints.append(checkpoints_by_state)
    return checkpoints
# return checkpoints =
# [[[253.75, 43.0], [286.5, 43.0], [319.25, 43.0], [448.25, 43.0], [480.5, 43.0], [512.75, 43.0]],
#  [[263.25, 43.0], [291.5, 43.0], [319.75, 43.0], [450.5, 43.0], [487.0, 43.0], [523.5, 43.0]],
#  [[242.75, 43.0], [278.5, 43.0], [314.25, 43.0], [446.75, 43.0], [475.5, 43.0], [504.25, 43.0]]]


# default or mypinch or yourpinch
# 0 = default, 1 = friend, 2 = enemy
# frame = bgr
def setup_color_list(frame, checkpoints):
    color_list = list()
    marker_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    for state_num in range(len(checkpoints)):
        state = checkpoints[state_num]
        color_list_by_state = list()
        for points in range(len(state)):
            color = frame[state[points][1], state[points][0], :]
            color_list_by_state.append(np.array(color))
            cv2.drawMarker(frame, np.array(
                state[points]), marker_color[state_num], markerSize=5)
        color_list.append(color_list_by_state)
    return color_list


# 3つの要素の内、一つだけ正しいのがある
def judge_pinch_team(color_list):
    state = ["default", "friend", "enemy"]
    for state_num in range(len(color_list)):
        float_means = np.mean(color_list[state_num], axis=1)
        int_means = np.floor(float_means)
        # print(state[state_num], "= ", np.all(int_means < 100))
        if np.all(int_means < 100):
            return state_num


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/asari_trim.mp4')
    # movie = cv2.VideoCapture('./data/video/pinch/area_default_only.mp4')
    # movie = cv2.VideoCapture('./data/video/pinch/area_mypinch_only.mp4')
    # movie = cv2.VideoCapture('./data/video/pinch/area_yourpinch_only.mp4')

    # json読み込みと変換
    position = open('config/json/position.json', 'r')
    checkpoints = setup_checkpoints(position)

    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        # 0 = default, 1 = friend, 2 = enemy
        color_list = setup_color_list(frame, checkpoints)
        is_pinch = judge_pinch_team(color_list)
        print(is_pinch)

        # default, friend
        # cv2.rectangle(frame, (219, 39), (352, 47), (255, 0, 0), 1)
        # friend_pinch, friend
        # cv2.rectangle(frame, (234, 39), (348, 47), (0, 255, 0), 1)
        # enemy_pinch, friend
        # cv2.rectangle(frame, (205, 39), (352, 47), (0, 0, 255), 1)

        if cv2.waitKey(1) == 27:
            break

        cv2.imshow('frame', frame)
        time.sleep(0.02)

    movie.release()
