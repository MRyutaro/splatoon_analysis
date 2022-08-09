import cv2
import json
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import toml


def main():
    open_position = open('config/position.json', 'r')
    position = json.load(open_position)
    open_color = open('config/color.json', 'r')
    color = json.load(open_color)

    movie = cv2.VideoCapture(capture_mode_setting())
    frame_width, frame_height = position["frame_size"]["width"], position["frame_size"]["height"]

    my_team_range = [[position["icon"]["my"]["min"]["x"],
                     position["icon"]["my"]["min"]["y"]],
                     [position["icon"]["my"]["max"]["x"],
                     position["icon"]["my"]["max"]["y"]]]
    # opponent_team_range = [[position["icon"]["your"]["min"]["x"],
    #                        position["icon"]["your"]["min"]["y"]],
    #                        [position["icon"]["your"]["max"]["x"],
    #                        position["icon"]["your"]["max"]["y"]]]

    my_icons_range = setup_icons_range(my_team_range)
    # opponent_icons_range = setup_icons_range(opponent_team_range)

    ink_color = color["purple"]["hue"]
    color_range = color["purple"]["range"]

    my_team_condition = ["alive", "alive", "alive", "alive"]
    # opponent_team_condition = ["alive", "alive", "alive", "alive"]

    is_gaming = False
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))
        binary_image = change_color2white(frame, ink_color, color_range)

        if is_gaming is True:
            for person in range(len(my_icons_range)):
                clipped_frame = binary_image[my_icons_range[person][0][1]:my_icons_range[person][1][1],
                                             my_icons_range[person][0][0]:my_icons_range[person][1][0]]
                unique, counts = np.unique(clipped_frame, return_counts=True)
                print(unique, counts)
                # result = np.column_stack((unique, counts))
                # print(f"{person+1}人目:{result[1]}", end=" ")
                # if result[1][1] >= 200:
                #     my_team_condition[person] = "alive"
                # elif result[1][1] < 200:
                #     my_team_condition[person] = "SP"
            print(my_team_condition)

        draw_icons(frame, my_icons_range)
        # draw_icons(frame, opponent_icons_range)

        cv2.imshow('frame', cv2.resize(frame, (960, 540)))
        cv2.waitKey(1)
        sleep(0.1)

    movie.release()


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

    persons_range = []
    for person in range(4):
        min = [int((icon_width/4)*person+team_range[0][0]),
               team_range[0][1]]
        max = [int((icon_width/4)*(person+1) +
                   team_range[0][0]), team_range[1][1]]
        person_range = [min, max]
        persons_range.append(person_range)
    return persons_range


def draw_icons(frame, icons_range):
    for person in range(len(icons_range)):
        cv2.rectangle(
            frame,
            (icons_range[person][0][0], icons_range[person][0][1]),
            (icons_range[person][1][0], icons_range[person][1][1]),
            (255, 0, 0), 1)


def change_color2white(raw_image, color, color_range):
    # settings
    raw_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
    cmp_color = color-85
    h_lower = int(color-color_range/2)
    h_upper = int(color+color_range/2)
    hsv_lower = np.array([int(h_lower), 0, 0])
    hsv_upper = np.array([int(h_upper), 255, 255])

    # h_binarization
    hsv_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2HSV)
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


def extract_contours(binary_image, contours_area_lower):
    # 輪郭抽出
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # フィルタ
    contours = list(filter(lambda x: cv2.contourArea(x)
                    > contours_area_lower, contours))

    return contours


if __name__ == "__main__":
    main()
