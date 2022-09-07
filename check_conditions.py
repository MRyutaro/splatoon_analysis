import cv2
import json
import numpy as np
import statistics


class CheckConditions():
    def __init__(self, team: str):
        # print("init")
        self.team = team
        self.all_icons_ranges = self.__read_json()
        # print(self.all_icons_ranges)
        # ここで4分割にしておく

    def __read_json(self):
        # print("json読みこみ")
        open_json = open("config/json/position.json")
        read_json = json.load(open_json)
        icons = read_json["icons"][f"{self.team}_icons_range"]
        return icons

    def check_conditions(self, image, pinch_team: str = "None") -> list:
        team_icons_range = self.__decide_icons_range(pinch_team)
        # print(team_icons_range)
        personal_icon_ranges = self.__create_check_ranges(
            image, team_icons_range)
        # print(personal_icon_ranges)
        binary_image = self._binarize_image(130, 255)

        conditions = []
        for person in range(4):
            clipped_frame = image[personal_icon_ranges[person][0][1]:personal_icon_ranges[person][1][1],
                                  personal_icon_ranges[person][0][0]:personal_icon_ranges[person][1][0]]
            unique, counts = np.unique(binary_image, return_counts=True)
            result = np.column_stack((unique, counts))
            if len(result) > 1:
                if result[1][1] >= 250:
                    conditions.append("ALIVE")
                else:
                    hsv_clipped_frame = cv2.cvtColor(
                        clipped_frame, cv2.COLOR_RGB2HSV)
                    s_mode = statistics.mode(
                        hsv_clipped_frame[:, :, 2].flatten())
                    print(f"{person}人目は{s_mode}です", end="\t")
                    if s_mode < 100:
                        conditions.append("DEATH")
                    else:
                        conditions.append("SPECIAL")
        print(conditions)
        return conditions

    def __decide_icons_range(self, pinch_team: str) -> dict:
        # print("アイコンの範囲を決定")
        if pinch_team == "None":
            default_icons_ranges = self.all_icons_ranges["default"]
            return default_icons_ranges
        elif pinch_team == "friend":
            icons_range_in_friend_pinch = self.all_icons_ranges["friend_is_in_pinch"]
            return icons_range_in_friend_pinch
        else:
            icons_range_in_enemy_pinch = self.all_icons_ranges["enemy_is_in_pinch"]
            return icons_range_in_enemy_pinch

    def __create_check_ranges(self, image, team_icons_range: dict) -> list:
        team_range_min = list(team_icons_range["min"].values())
        team_range_max = list(team_icons_range["max"].values())
        self.__draw_rectangle(image, [team_range_min, team_range_max])
        team_range_width = team_range_max[0] - team_range_min[0]
        team_range_height = team_range_max[1] - team_range_min[1]
        # print(team_range_width, team_range_height)

        # ここfor文回したくない。めっちゃ遅くなる可能性。
        personal_icon_ranges = []
        for person in range(4):
            personal_icon_min = [team_range_min[0] + int((team_range_width/4)*person + int(team_range_width/32)),
                                 team_range_min[1] + int(team_range_height/8)]
            personal_icon_max = [team_range_min[0] + int((team_range_width/4)*(person+1) - int(team_range_width/32)),
                                 team_range_max[1] - int(team_range_height/8)]
            personal_icon_range = [personal_icon_min, personal_icon_max]
            self.__draw_rectangle(image, personal_icon_range)
            personal_icon_ranges.append(personal_icon_range)
        return personal_icon_ranges

    def _binarize_image(self, min, max):
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(
            gray_image, 130, 255, cv2.THRESH_BINARY)
        return binary_image

    def __draw_rectangle(self, image, range: list):
        # print("iconの範囲を描画")
        print(range)
        cv2.rectangle(image, (range[0]), (range[1]), (0, 0, 255), 1)


if __name__ == "__main__":
    friend_check_conditions = CheckConditions("friend")
    enemy_check_conditions = CheckConditions("enemy")

    # image_path = "./data/image/default.png"
    # image_path = "./data/image/pinch/friend/8.png"
    image_path = "./data/image/pinch/enemy/0.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))

    friend_check_conditions.check_conditions(image, "enemy")

    cv2.imshow("image", image)
    if cv2.waitKey(0) == 27:
        exit()
