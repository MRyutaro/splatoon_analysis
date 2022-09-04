import cv2
import time
from image_recognition_v1 import ImageRecognition

if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    game_start = ImageRecognition("game", "starts", 0.8)
    game_finish = ImageRecognition("game", "finishes", 0.8)
    map_is_opened = ImageRecognition("map", "is opened", 0.9)

    is_gaming = False
    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        # ゲームが進行中じゃなかったら
        if not is_gaming:
            if game_start.is_equal(frame):
                is_gaming = True

        # ゲームが進行中だったら
        else:
            if not map_is_opened.is_equal(frame):
                print("ピンチの条件分岐")
            else:
                print("マップ開いてる時の処理")
            if game_finish.is_equal(frame):
                is_gaming = False

        # print(is_gaming)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
