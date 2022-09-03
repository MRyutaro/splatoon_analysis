import cv2
import numpy as np
import time


class CheckIsMaping():
    def __init__(self):
        self.map_range = self.read_json()

    def read_json(self):
        return [["left", [45, 205], [50, 222], 255],
                ["top", [309, 40], [329, 44], 255],
                ["right", [587, 204], [591, 225], 255]]

    def is_maping(self, frame):
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
        self.show_rectangle(frame, self.map_range)
        for i in range(len(self.map_range)):
            if not self.is_one_color(
                    binary, self.map_range[i][1], self.map_range[i][2], self.map_range[i][3]):
                return False
        return True

    def show_rectangle(self, frame, map_range):
        for i in range(len(map_range)):
            cv2.rectangle(frame, (map_range[i][1]),
                          (map_range[i][2]), (255, 0, 0), 1)

    def is_one_color(self, binary, min, max, color):
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
    check_is_maping = CheckIsMaping()

    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        if check_is_maping.is_maping(frame):
            print("map is opening")
        else:
            print("map is closing")

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
