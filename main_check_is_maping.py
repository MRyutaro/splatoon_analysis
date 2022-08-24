import cv2
import numpy as np
import time


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


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/asari.mp4')

    is_maping = False
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        is_maping = check_is_maping(frame)
        if is_maping is True:
            print("map is opening")
        else:
            print("map is closing")

        map_range = [["left", [45, 205], [50, 222]],
                     ["top", [309, 40], [329, 44]],
                     ["right", [587, 204], [591, 225]]]
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
        for i in range(len(map_range)):
            cv2.rectangle(
                frame, (map_range[i][1]), (map_range[i][2]), (255, 0, 0), 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break

        time.sleep(0.02)

    movie.release()