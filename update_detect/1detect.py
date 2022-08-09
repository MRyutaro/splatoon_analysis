import cv2
import json
from time import sleep
import toml


def main():
    open_position = open('config/position.json', 'r')
    position = json.load(open_position)
    # open_color = open('config/color.json', 'r')
    # color = json.load(open_color)

    movie = cv2.VideoCapture(capture_mode_setting())
    frame_width, frame_height = position["frame_size"]["width"], position["frame_size"]["height"]

    my_team_range = [[position["icon"]["my"]["min"]["x"],
                     position["icon"]["my"]["min"]["y"]],
                     [position["icon"]["my"]["max"]["x"],
                     position["icon"]["my"]["max"]["y"]]]
    opponent_team_range = [[position["icon"]["your"]["min"]["x"],
                           position["icon"]["your"]["min"]["y"]],
                           [position["icon"]["your"]["max"]["x"],
                           position["icon"]["your"]["max"]["y"]]]

    my_icons_range = setup_icons_range(my_team_range)
    opponent_icons_range = setup_icons_range(opponent_team_range)

    # ink_color = color["purple"]["hue"]
    # color_range = color["purple"]["range"]

    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))

        cv2.rectangle(
            frame, (my_team_range[0][0], my_team_range[0][1]), (my_team_range[1][0], my_team_range[1][1]), (255, 0, 0), 1)
        cv2.rectangle(
            frame, (opponent_team_range[0][0], opponent_team_range[0][1]), (opponent_team_range[1][0], opponent_team_range[1][1]), (255, 0, 0), 1)
        draw_icons(frame, my_icons_range)
        draw_icons(frame, opponent_icons_range)

        cv2.imshow('frame', cv2.resize(frame, (960, 540)))
        cv2.waitKey(1)
        sleep(0.05)

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


if __name__ == "__main__":
    main()
