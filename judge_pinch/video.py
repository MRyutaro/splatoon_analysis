import cv2
import statistics
import time


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


def judge_pinch():
    pass


# 黒のポイントを作ってあげる。単に4分割する。
def setup_check_points(team_range):
    pass


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_mypinch.mp4')

    before = None
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        cv2.rectangle(frame, (235, 20), (348, 50), (255, 0, 0), 1)
        cv2.rectangle(frame, (414, 17), (560, 53), (255, 0, 0), 1)

        if cv2.waitKey(1) == 27:
            break

        cv2.imshow('frame', frame)
        time.sleep(0.03)

    movie.release()
