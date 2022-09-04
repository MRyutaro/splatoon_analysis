import cv2
import numpy as np
import time
import json


class ImageRecognition():
    def __init__(self, game_transition: str, label: str, correct_rate: float):
        self.game_transition = game_transition
        self.label = label
        self.threshold, self.range = self.read_json(
            game_transition, label)
        self.correct_rate = correct_rate

    def read_json(self, game_transition: str, label: str):
        open_json = open(f"config/json/{game_transition}.json")
        read_json = json.load(open_json)
        return read_json[game_transition][label]["threshold"], read_json[game_transition][label]["range"]

    def is_equal(self, image):
        self.show_rectangle(image)
        binary_image = self.binary(image)
        for i in range(len(self.range)):
            clipped_image = self.clip_image(
                binary_image, self.range[i]["target"][0], self.range[i]["target"][1])
            if not self.check_color(clipped_image, self.range[i]["color"]):
                # Falseのときに実行するクラス
                return False
        return True

    def show_rectangle(self, image):
        for i in range(len(self.range)):
            cv2.rectangle(image, (self.range[i]["target"][0]),
                          (self.range[i]["target"][1]), (255, 0, 0), 1)

    def binary(self, image):
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(
            gray_image, self.threshold[0], self.threshold[1], cv2.THRESH_BINARY)
        return binary

    def clip_image(self, binary_image, min, max):
        clipped_image = binary_image[min[1]:max[1], min[0]:max[0]]
        return clipped_image

    def check_color(self, clipped_image, color):
        size = self.check_size(color)
        if np.count_nonzero(clipped_image == color) > self.correct_rate*size:
            return True

    def check_size(self, color):
        size = len(color[0])*len(color)
        return size


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    game_start = ImageRecognition("game", "starts", 0.9)

    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        print(game_start.is_equal(frame))

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
