import cv2
import time

from image_recognition_v1 import ImageRecognition

if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    game_start = ImageRecognition("game", "starts")

    is_gaming = False
    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        print(is_gaming)
        if not is_gaming:
            if game_start.is_equal(frame):
                is_gaming = True

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
