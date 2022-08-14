import cv2
import numpy as np
import time


def check_is_maping(frame):
    check_range = [["left", [45, 205], [50, 222]],
                   ["top", [309, 40], [329, 44]],
                   ["right", [587, 204], [591, 225]],
                   ["down", [309, 387], [329, 392]]]
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

    for i in range(4):
        if check_is_maping_by_range(
                binary, check_range[i][0], check_range[i][1], check_range[i][2]) is False:
            return False
    return True


def check_is_maping_by_range(binary, icon_name, min, max):
    clipped_range = binary[min[1]:max[1], min[0]:max[0]]
    unique, counts = np.unique(clipped_range, return_counts=True)
    result = np.column_stack((unique, counts))
    # print(icon_name, "\t", result)
    # cv2.imshow(icon_name, clipped_range)
    # if cv2.waitKey(0) == 27:
    #     exit()
    if len(result) == 1:
        if result[0][0] == 255:
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

        check_range = [["left", [45, 205], [50, 222]],
                       ["top", [309, 40], [329, 44]],
                       ["right", [587, 204], [591, 225]],
                       ["down", [309, 387], [329, 392]]]
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
        for i in range(4):
            cv2.rectangle(binary, (check_range[i][1]), (check_range[i][2]), (255, 0, 0), 1)
        cv2.imshow('frame', cv2.resize(frame, (1920, 1080)))
        if cv2.waitKey(1) == 27:
            break

        time.sleep(0.02)

    movie.release()
