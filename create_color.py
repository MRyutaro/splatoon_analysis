import cv2
import time
import json
import numpy as np


# この関数があまりよろしくない。関数名だけ見て戻り値が何なのか分からない。
def read_json(game_transition: str, label: str):
    open_json = open(f"config/json/{game_transition}.json")
    read_json = json.load(open_json)
    thresholds = read_json[game_transition][label]["threshold"]
    recognition_data = read_json[game_transition][label]["range"]
    # print(thresholds)
    # print(recognition_data)
    return thresholds, recognition_data


# これはけちらずにrangeじゃなくてmin, maxと書いた方がいいかも。
def binary(image, range):
    bgr_frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(
        gray_frame, range[0], range[1], cv2.THRESH_BINARY)
    return binary


def show_rectangle(image, min, max):
    # print("四角形を描画")
    cv2.rectangle(image, min, max, (0, 0, 0), 1)


def clip_image(image, recognition_range):
    # print("画像の切り取り")
    # print(recognition_range)
    for i in range(len(recognition_range)):
        min = recognition_range[i]["target"][0]
        max = recognition_range[i]["target"][1]
        clipped_image = image[min[1]:max[1],
                              min[0]:max[0]]
        get_color_from(clipped_image, i)
        show_rectangle(image, min, max)


def get_color_from(clipped_image, i):
    # print("色のデータを取得")
    print(f"{i+1}番目の範囲------------------------")
    print("横の長さ", len(clipped_image[0]))
    print("縦の長さ", len(clipped_image))
    output(clipped_image)


def output(clipped_image):
    clipped_image = clipped_image.tolist()
    print(type(clipped_image))
    data = {"color": clipped_image}
    with open('data/tmp.json', 'a') as f:
        json.dump(data, f)


if __name__ == "__main__":
    # ゲーム開始
    # image_path = "./data/image/start.png"
    # image = cv2.imread(image_path)
    # image = cv2.resize(image, (768, 432))
    # game_start = read_json("game", "starts")
    # image = binary(image, game_start[0])
    # clip_image(image, game_start[1])

    # ゲーム終了
    # image_path = "./data/image/finish1.png"
    # image = cv2.imread(image_path)
    # image = cv2.resize(image, (768, 432))
    # game_finish = read_json("game", "finishes")
    # image = binary(image, game_finish[0])
    # clip_image(image, game_finish[1])

    # map
    # image_path = "./data/image/map.png"
    # image = cv2.imread(image_path)
    # image = cv2.resize(image, (768, 432))
    # map = read_json("map", "is opened")
    # image = binary(image, map[0])
    # clip_image(image, map[1])

    # friend is in pinch
    # 画像を大量に
    # frame_num = 9
    # for i in range(frame_num):
    #     image_path = f"./data/image/pinch/friend/{i}.png"
    #     image = cv2.imread(image_path)
    #     image = cv2.resize(image, (768, 432))
    #     friend_is_in_pinch = read_json("in_pinch", "is friend")
    #     image = binary(image, friend_is_in_pinch[0])
    #     clip_image(image, friend_is_in_pinch[1])

    # enemy is in pinch
    # 画像を大量に
    frame_num = 9
    for i in range(frame_num):
        image_path = f"./data/image/pinch/enemy/{i}.png"
        image = cv2.imread(image_path)
        image = cv2.resize(image, (768, 432))
        enemy_is_in_pinch = read_json("in_pinch", "is enemy")
        image = binary(image, enemy_is_in_pinch[0])
        clip_image(image, enemy_is_in_pinch[1])

    # cv2.imshow("image", image)
    # if cv2.waitKey(0) == 27:
    #     exit()
