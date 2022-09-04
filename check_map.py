import cv2
import time

from image_recognition_v1 import ImageRecognition

if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')
    map_is_opened = ImageRecognition("map", "is opened", 0.9)

    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        print(map_is_opened.is_equal(frame))

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
