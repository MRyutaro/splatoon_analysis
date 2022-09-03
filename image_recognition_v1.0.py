import cv2
import numpy as np
import time
import json


class ImageRecognition():
    def __init__(self, game_transition: str, label: str):
        self.game_transition = game_transition
        self.label = label
        self.threshold, self.range = self.read_json(
            game_transition, label)

    def read_json(self, game_transition: str, label: str):
        open_json = open(f"config/json/{game_transition}.json")
        read_json = json.load(open_json)
        return read_json[game_transition][label]["threshold"], read_json[game_transition][label]["range"]

    def is_equal(self, frame):
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(
            gray_frame, self.threshold[0], self.threshold[1], cv2.THRESH_BINARY)
        self.show_rectangle(frame)
        for i in range(len(self.range)):
            if not self.is_one_color(
                    binary, self.range[i]["target"][0], self.range[i]["target"][1], self.range[i]["color"]):
                return False
        print(f"{self.game_transition} {self.label}")
        return True

    def show_rectangle(self, frame):
        for i in range(len(self.range)):
            cv2.rectangle(frame, (self.range[i]["target"][0]),
                          (self.range[i]["target"][1]), (255, 0, 0), 1)

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
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    map_is_opend = ImageRecognition("map", "is opened")
    game_starts = ImageRecognition("game", "starts")

    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        # if not game_starts.is_equal(frame):
        #     print("game finish")
        if not map_is_opend.is_equal(frame):
            print("map is closing")

        cv2.rectangle(frame, (175, 16), (220, 33), (255, 0, 0), 1)
        cv2.rectangle(frame, (545, 16), (590, 33), (255, 0, 0), 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
