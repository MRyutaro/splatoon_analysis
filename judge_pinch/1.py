import cv2
import time
import json


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


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area.mp4')
    fps = movie.get(cv2.CAP_PROP_FPS)
    sec_per_frame = 1/fps
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

    while True:
        excution_start_time = time.time()
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

        if cv2.waitKey(1) == 27:
            break

        cv2.imshow('frame', cv2.resize(frame, (960, 540)))
        execution_time = time.time() - excution_start_time
        if execution_time < sec_per_frame:
            time.sleep(sec_per_frame - execution_time)

    movie.release()
