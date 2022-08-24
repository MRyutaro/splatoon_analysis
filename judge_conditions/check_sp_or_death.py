import cv2
import time
import json
import statistics
import pandas as pd
import itertools
import os


def setup_icons_range(team_range):
    icon_width = team_range[1][0]-team_range[0][0]
    icon_height = team_range[1][1]-team_range[0][1]

    persons_range = []
    for person in range(4):
        min = [team_range[0][0] + int((icon_width/4)*person + int(icon_width/16)),
               team_range[0][1] + int(icon_height/8)]
        max = [team_range[0][0] + int((icon_width/4)*(person+1) - int(icon_width/16)),
               team_range[1][1] - int(icon_height/10)]
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


def check_hsv(frame, icons_range):
    hsv_modes = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for person in range(len(icons_range)):
        clipped_frame = frame[icons_range[person][0][1]:icons_range[person][1][1],
                              icons_range[person][0][0]:icons_range[person][1][0]]
        hsv_clipped_frame = cv2.cvtColor(clipped_frame, cv2.COLOR_RGB2HSV)
        person_hsv_mode = [statistics.mode(hsv_clipped_frame[:, :, 0].flatten()),
                           statistics.mode(
                               hsv_clipped_frame[:, :, 1].flatten()),
                           statistics.mode(hsv_clipped_frame[:, :, 2].flatten())]
        hsv_modes[person] = person_hsv_mode
    hsv_modes = list(itertools.chain.from_iterable(hsv_modes))
    return hsv_modes


def save_to_csv(all_data, csv_path):
    columns_name = ["frame_count",
                    "1-h", "1-s", "1-v",
                    "2-h", "2-s", "2-v",
                    "3-h", "3-s", "3-v",
                    "4-h", "4-s", "4-v"]
    if os.path.isdir(csv_path) is True:
        os.remove(csv_path)
    df = pd.DataFrame(all_data, columns=columns_name, dtype=object)
    df.to_csv(csv_path, index=False, encoding='UTF_8')


if __name__ == "__main__":
    open_position = open('config/json/position.json', 'r')
    position = json.load(open_position)
    my_team_range = [[position["icon"]["my"]["min"]["x"],
                     position["icon"]["my"]["min"]["y"]],
                     [position["icon"]["my"]["max"]["x"],
                     position["icon"]["my"]["max"]["y"]]]
    opponent_team_range = [[position["icon"]["your"]["min"]["x"],
                           position["icon"]["your"]["min"]["y"]],
                           [position["icon"]["your"]["max"]["x"],
                           position["icon"]["your"]["max"]["y"]]]

    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/asari_cut.mp4')
    fps = movie.get(cv2.CAP_PROP_FPS)

    # fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # writer = cv2.VideoWriter('hsv_data/asari_cut.mp4', fmt, fps, (960, 540))

    frame_count = 0
    all_my_team_hsv = list()
    all_opponent_team_hsv = list()
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))
        my_icons_range = setup_icons_range(my_team_range)
        opponent_icons_range = setup_icons_range(opponent_team_range)
        # draw
        draw_icons(frame, my_icons_range)
        draw_icons(frame, opponent_icons_range)
        cv2.rectangle(frame,
                      (my_team_range[0][0], my_team_range[0][1]),
                      (my_team_range[1][0], my_team_range[1][1]),
                      (0, 0, 255), 1)
        cv2.rectangle(frame,
                      (opponent_team_range[0][0], opponent_team_range[0][1]),
                      (opponent_team_range[1][0], opponent_team_range[1][1]),
                      (0, 0, 255), 1)
        cv2.rectangle(frame,
                      (344, 80),
                      (420, 150),
                      (255, 255, 255), -1)
        cv2.putText(frame,
                    f"{frame_count}",
                    org=(354, 120),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0, 0, 0),
                    thickness=2,
                    lineType=cv2.LINE_4)

        my_team_hsv = check_hsv(frame, my_icons_range)
        my_team_hsv.insert(0, frame_count)
        print("my--------", my_team_hsv)
        # all_my_team_hsv.append(my_team_hsv)
        # save_to_csv(all_my_team_hsv, "hsv_data/my_team_hsv.csv")

        # opponent_team_hsv = check_hsv(frame, opponent_icons_range)
        # opponent_team_hsv.insert(0, frame_count)
        # # print("opponent--", opponent_team_hsv)
        # all_opponent_team_hsv.append(opponent_team_hsv)
        # save_to_csv(all_opponent_team_hsv, "hsv_data/opponent_team_hsv.csv")

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            exit()
        time.sleep(0.028)
        # writer.write(frame)
        frame_count += 1

    movie.release()
    cv2.destroyAllWindows()
