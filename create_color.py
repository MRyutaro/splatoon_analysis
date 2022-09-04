import cv2
import time


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_trim1.mp4')

    while movie.isOpened:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))

        if cv2.waitKey(1) == 27:
            break

        cv2.imshow('frame', frame)
        time.sleep(0.03)

    movie.release()
