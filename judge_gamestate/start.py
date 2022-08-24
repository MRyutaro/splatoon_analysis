import cv2
import numpy as np
import time


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

    is_gaming = False
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        if is_gaming is False:
            is_gaming = check_start_game(frame)
        print(is_gaming)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
