import cv2
import time
from image_recognition_v1 import ImageRecognition
from check_pinch import CheckPinch
from check_conditions import CheckConditions


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    game_start = ImageRecognition("game", "starts")
    game_finish = ImageRecognition("game", "finishes")
    map_is_opened = ImageRecognition("map", "is opened", 0.9)

    friend_is_in_pinch = CheckPinch("is friend")
    enemy_is_in_pinch = CheckPinch("is enemy")

    check_friend_conditions = CheckConditions("friend")
    check_enemy_conditions = CheckConditions("enemy")

    is_gaming = False
    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        # ゲームが進行中じゃなかったら
        if not is_gaming:
            print("ゲーム停止中")
            if game_start.is_equal(frame):
                is_gaming = True

        # ゲームが進行中だったら
        else:
            if not map_is_opened.is_equal(frame):
                if friend_is_in_pinch.is_equal(frame):
                    friend_conditions = check_friend_conditions.check_conditions(frame, "friend")
                    enemy_conditions = check_enemy_conditions.check_conditions(frame, "friend")
                elif enemy_is_in_pinch.is_equal(frame):
                    friend_conditions = check_friend_conditions.check_conditions(frame, "enemy")
                    enemy_conditions = check_enemy_conditions.check_conditions(frame, "enemy")
                else:
                    friend_conditions = check_friend_conditions.check_conditions(frame)
                    enemy_conditions = check_enemy_conditions.check_conditions(frame)
                print(friend_conditions, enemy_conditions)
            if game_finish.is_equal(frame):
                is_gaming = False

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
