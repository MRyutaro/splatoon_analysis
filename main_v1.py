import cv2
import json
import math
import numpy as np
import statistics
import time
import toml


def main():
    open_position = open('config/json/position.json', 'r')
    position = json.load(open_position)
    open_color = open('config/json/color.json', 'r')
    color = json.load(open_color)

    movie = cv2.VideoCapture(capture_mode_setting())
    fps = movie.get(cv2.CAP_PROP_FPS)
    sec_per_frame = 1/fps
    frame_width, frame_height = position["frame_size"]["width"], position["frame_size"]["height"]

    my_team_range = [[position["icon"]["generally"]["my"]["min"]["x"],
                     position["icon"]["generally"]["my"]["min"]["y"]],
                     [position["icon"]["generally"]["my"]["max"]["x"],
                     position["icon"]["generally"]["my"]["max"]["y"]]]
    # opponent_team_range = [[position["icon"]["generally"]["your"]["min"]["x"],
    #                        position["icon"]["generally"]["your"]["min"]["y"]],
    #                        [position["icon"]["generally"]["your"]["max"]["x"],
    #                        position["icon"]["generally"]["your"]["max"]["y"]]]

    my_team_condition = ["ALIVE", "ALIVE", "ALIVE", "ALIVE"]
    # opponent_team_condition = ["ALIVE", "ALIVE", "ALIVE", "ALIVE"]

    # インクカラーを推定して自動判定したい。
    ink_color = color["purple"]["hue"]
    color_range = color["purple"]["range"]
    color = [ink_color, color_range]

    is_gaming = False
    is_maping = False
    game_start_time = 0
    game_time = 0
    while True:
        excution_start_time = time.time()
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))

        if is_gaming is False:
            print("Not in game")
            is_gaming = check_start_game(frame)
            if is_gaming is True:
                game_start_time = time.time()
        else:
            game_time = math.floor(time.time()-game_start_time)
            # ガチマッチの場合(300-10)秒くらいに設定しておく。
            if game_start_time != 0 and game_time > 290:
                is_gaming = check_finish_game(frame)

            is_maping = check_is_maping(frame)
            if is_maping is True:
                print(game_time, "\t", "Opening map.")
            else:
                my_team_condition = judge_conditions(
                    frame, my_team_range, my_team_condition, color)
                print(game_time, "\t", my_team_condition)

        cv2.imshow('frame', cv2.resize(frame, (960, 540)))
        if cv2.waitKey(1) == 27:
            exit()
        execution_time = time.time() - excution_start_time
        if execution_time < sec_per_frame:
            time.sleep(sec_per_frame - execution_time)

    movie.release()


# setup-----------------------------------
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


def setup_icons_range(team_range):
    icon_width = team_range[1][0]-team_range[0][0]
    icon_height = team_range[1][1]-team_range[0][1]

    persons_range = []
    for person in range(4):
        min = [team_range[0][0] + int((icon_width/4)*person + int(icon_width/32)),
               team_range[0][1] + int(icon_height/8)]
        max = [team_range[0][0] + int((icon_width/4)*(person+1) - int(icon_width/32)),
               team_range[1][1] - int(icon_height/8)]
        person_range = [min, max]
        persons_range.append(person_range)
    return persons_range


# draw-------------------------------------
def draw_icons(frame, icons_range):
    for person in range(len(icons_range)):
        cv2.rectangle(
            frame,
            (icons_range[person][0][0], icons_range[person][0][1]),
            (icons_range[person][1][0], icons_range[person][1][1]),
            (255, 0, 0), 1)


# check------------------------------------
def check_start_game(frame):
    start_range = [["area1", [1, 2], [16, 3], 0],
                   ["area2", [1, 2], [3, 20], 0],
                   ["area3", [1, 19], [17, 22], 0],
                   ["area4", [11, 8], [12, 9], 0],
                   ["area5", [4, 12], [6, 13], 0],
                   ["area6", [6, 5], [11, 6], 255],
                   ["area7", [5, 6], [7, 9], 255],
                   ["area8", [10, 12], [11, 15], 255],
                   ["area9", [6, 15], [10, 16], 255]]
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)
    minute_image = binary[27:49, 363:380]
    for i in range(len(start_range)):
        if check_whether_one_color(
                minute_image, start_range[i][1], start_range[i][2], start_range[i][3]) is False:
            return False
    return True


def check_finish_game(frame):
    finish_range = [["upper_left", [35, 43], [87, 68], 255],
                    ["upper_right", [549, 28], [581, 41], 255],
                    ["botton_left", [29, 282], [154, 298], 255],
                    ["bottom_right", [508, 364], [610, 383], 255]]
    binary = change_hcolor2white(frame, 140, 30)
    for i in range(len(finish_range)):
        if check_whether_one_color(
                binary, finish_range[i][1], finish_range[i][2], finish_range[i][3]) is False:
            return True
    return False


def check_is_maping(frame):
    map_range = [["left", [45, 205], [50, 222], 255],
                 ["top", [309, 40], [329, 44], 255],
                 ["right", [587, 204], [591, 225], 255]]
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

    for i in range(len(map_range)):
        if check_whether_one_color(
                binary, map_range[i][1], map_range[i][2], map_range[i][3]) is False:
            return False
    return True


def check_whether_one_color(binary, min, max, color):
    clipped_range = binary[min[1]:max[1], min[0]:max[0]]
    unique, counts = np.unique(clipped_range, return_counts=True)
    result = np.column_stack((unique, counts))
    if len(result) == 1:
        if result[0][0] == color:
            return True
        else:
            return False
    else:
        return False


def change_hcolor2white(frame, hcolor, hcolor_range):
    # settings
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cmp_color = hcolor-85
    h_lower = int(hcolor-hcolor_range/2)
    h_upper = int(hcolor+hcolor_range/2)
    hsv_lower = np.array([int(h_lower), 0, 0])
    hsv_upper = np.array([int(h_upper), 255, 255])

    # h_binarization
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    extracted_image = np.copy(hsv_image)
    extracted_image[:, :, 0] = np.where(extracted_image[:, :, 0] < h_lower,  # type: ignore
                                        cmp_color,
                                        extracted_image[:, :, 0])
    extracted_image[:, :, 0] = np.where(extracted_image[:, :, 0] > h_upper,  # type: ignore
                                        cmp_color,
                                        extracted_image[:, :, 0])

    hsv_mask = cv2.inRange(extracted_image, hsv_lower, hsv_upper)
    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=hsv_mask)
    bgr_image = cv2.cvtColor(masked_image, cv2.COLOR_HSV2BGR)
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

    # binarization
    _, binary = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY)
    return binary


def judge_conditions(frame, team_range, conditions, color):
    my_icons_range = setup_icons_range(team_range)
    draw_icons(frame, my_icons_range)
    for person in range(len(my_icons_range)):
        clipped_frame = frame[my_icons_range[person][0][1]:my_icons_range[person][1][1],
                              my_icons_range[person][0][0]:my_icons_range[person][1][0]]
        binary_image = change_hcolor2white(clipped_frame, color[0], color[1])
        unique, counts = np.unique(binary_image, return_counts=True)
        result = np.column_stack((unique, counts))
        if len(result) > 1:
            if result[1][1] >= 250:
                conditions[person] = "ALIVE"
            elif result[1][1] < 250:
                hsv_clipped_frame = cv2.cvtColor(
                    clipped_frame, cv2.COLOR_RGB2HSV)
                s_mode = statistics.mode(hsv_clipped_frame[:, :, 2].flatten())
                print(f"{person}人目は{s_mode}です", end="\t")
                if s_mode < 100:
                    conditions[person] = "DEATH"
                else:
                    conditions[person] = "SP"
    return conditions


if __name__ == "__main__":
    main()
