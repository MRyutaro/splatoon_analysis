import cv2
import json
import numpy as np
import statistics
import time
from check_pinch import CheckPinch


class CheckConditions():
    def __init__(self, team: str):
        self.team = team
        self.all_icons_ranges = self.__read_json()
        self.saturation_standard_value = 200
        self.brightness_standard_value = 150

    def __read_json(self):
        open_json = open("config/json/position.json")
        read_json = json.load(open_json)
        icons = read_json["icons"][f"{self.team}_icons_range"]
        return icons

    def check_conditions(self, image, pinch_team: str = "None") -> list:
        team_icons_range = self.__decide_icons_range(pinch_team)
        team_range_min = list(team_icons_range["min"].values())
        team_range_max = list(team_icons_range["max"].values())
        team_range = [team_range_min, team_range_max]
        team_range_width = team_range_max[0] - team_range_min[0]
        team_range_height = team_range_max[1] - team_range_min[1]

        conditions = []
        for person in range(4):
            personal_icon_range = self.__create_check_ranges_of(
                person, image, team_range, team_range_width, team_range_height)
            clipped_frame = image[personal_icon_range[0][1]:personal_icon_range[1][1],
                                  personal_icon_range[0][0]:personal_icon_range[1][0]]
            hsv_clipped_frame = cv2.cvtColor(clipped_frame, cv2.COLOR_RGB2HSV)
            saturation_mean = statistics.mean(
                hsv_clipped_frame[:, :, 1].flatten())
            brightness_mean = statistics.mean(
                hsv_clipped_frame[:, :, 2].flatten())
            # print(f"{person+1}人目のsは{saturation_mean}です", end=" ")
            # print(f"{person+1}人目のvは{brightness_mean}です", end=" ")
            if saturation_mean > self.saturation_standard_value:
                self.__draw_rectangle(
                    image, personal_icon_range, [0, 0, 255], -1)
                conditions.append("ALIVE")
            else:
                if brightness_mean < self.brightness_standard_value:
                    self.__draw_rectangle(
                        image, personal_icon_range, [0, 0, 0], -1)
                    conditions.append("DEATH")
                else:
                    self.__draw_rectangle(
                        image, personal_icon_range, [255, 255, 255], -1)
                    conditions.append("SPECIAL")
        # print(conditions)
        print()
        return conditions

    def __decide_icons_range(self, pinch_team: str) -> dict:
        if pinch_team == "None":
            default_icons_ranges = self.all_icons_ranges["default"]
            return default_icons_ranges
        elif pinch_team == "friend":
            icons_range_in_friend_pinch = self.all_icons_ranges["friend_is_in_pinch"]
            return icons_range_in_friend_pinch
        else:
            icons_range_in_enemy_pinch = self.all_icons_ranges["enemy_is_in_pinch"]
            return icons_range_in_enemy_pinch

    def __create_check_ranges_of(self, person, image, team_range: list, team_range_width: int, team_range_height: int) -> list:
        team_range_min, team_range_max = team_range[:]
        personal_icon_min = [team_range_min[0] + int((team_range_width/4)*person + int(team_range_width/12)),
                             team_range_min[1] + int(2*team_range_height/3)]
        personal_icon_max = [team_range_min[0] + int((team_range_width/4)*(person+1) - int(team_range_width/12)),
                             team_range_max[1] - int(team_range_height/32)]
        personal_icon_range = [personal_icon_min, personal_icon_max]
        self.__draw_rectangle(image, personal_icon_range)
        return personal_icon_range

    def _binarize_image(self, image, min, max):
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(
            gray_image, min, max, cv2.THRESH_BINARY)
        cv2.imshow("image", binary_image)
        if cv2.waitKey(1) == 27:
            exit()
        return binary_image

    def __draw_rectangle(self, image, range: list, color: list = [0, 0, 255], thickness: int = 1):
        cv2.rectangle(image, (range[0]), (range[1]), color, thickness)


if __name__ == "__main__":
    friend_is_in_pinch = CheckPinch("is friend")
    enemy_is_in_pinch = CheckPinch("is enemy")
    check_friend_conditions = CheckConditions("friend")
    check_enemy_conditions = CheckConditions("enemy")

    # # image_path = "./data/image/default.png"
    # image_path = "./data/image/default_a2d1s1.png"
    # # image_path = "./data/image/pinch/friend/8.png"
    # # image_path = "./data/image/pinch/enemy/0.png"
    # image = cv2.imread(image_path)
    # image = cv2.resize(image, (768, 432))
    # friend_conditions = check_friend_conditions.check_conditions(image)
    # # friend_conditions = check_friend_conditions.check_conditions(image, "friend")
    # # friend_conditions = check_friend_conditions.check_conditions(image, "enemy")
    # cv2.imshow("image", image)
    # if cv2.waitKey(0) == 27:
    #     exit()

    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))
        # t = time.time()
        if friend_is_in_pinch.is_equal(frame):
            friend_conditions = check_friend_conditions.check_conditions(
                frame, "friend")
            enemy_conditions = check_enemy_conditions.check_conditions(
                frame, "friend")
        elif enemy_is_in_pinch.is_equal(frame):
            friend_conditions = check_friend_conditions.check_conditions(
                frame, "enemy")
            enemy_conditions = check_enemy_conditions.check_conditions(
                frame, "enemy")
        else:
            friend_conditions = check_friend_conditions.check_conditions(frame)
            enemy_conditions = check_enemy_conditions.check_conditions(frame)
        # print(time.time()-t)
        # print()
        cv2.imshow("image", frame)
        if cv2.waitKey(1) == 27:
            exit()
        time.sleep(0.02)
