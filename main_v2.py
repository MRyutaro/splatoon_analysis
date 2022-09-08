import cv2
import time
from image_recognition_v1 import ImageRecognition
from check_pinch import CheckPinch
from check_conditions import CheckConditions


if __name__ == "__main__":
    # settings
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    game_start = ImageRecognition("game", "starts")
    game_finish = ImageRecognition("game", "finishes")
    map_is_opened = ImageRecognition("map", "is opened", 0.9)
    friend_check_conditions = CheckConditions("friend")
    enemy_check_conditions = CheckConditions("enemy")

    friend_is_in_pinch = CheckPinch("is friend")
    enemy_is_in_pinch = CheckPinch("is enemy")
    friends_conditions = []
    enemies_conditions = []

    is_gaming = False
    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        # ゲームが進行中じゃなかったら
        if not is_gaming:
            print("ゲーム停止中", end=" | ")
            # t = time.time()
            if game_start.is_equal(frame):
                is_gaming = True
            # print(time.time()-t)

        # ゲームが進行中だったら
        else:
            print("ゲーム進行中", end=" | ")
            # マップを開いていたら
            if map_is_opened.is_equal(frame):
                print("マップ開いている", end=" | ")
            # マップを開いていなかったら
            else:
                print("マップ開いてない", end=" | ")
                if friend_is_in_pinch.is_equal(frame):
                    print("味方がピンチ！！", end="")
                elif enemy_is_in_pinch.is_equal(frame):
                    print("敵がピンチ！！！", end="")
                else:
                    print("デフォルト", end="")

            if game_finish.is_equal(frame):
                is_gaming = False

        print("\n")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
