import cv2
import time

from image_recognition_v1 import ImageRecognition

if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/finish.mp4')
    game_finishes = ImageRecognition("game", "finishes", 0.8)

    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        print(game_finishes.is_equal(frame))

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()