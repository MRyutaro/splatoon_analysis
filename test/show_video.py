import cv2
import time

# movie = cv2.VideoCapture(1)
movie = cv2.VideoCapture('./data/video/area.mp4')

while True:
    ret, frame = movie.read()
    if not ret:
        break

    frame = cv2.resize(frame, (768, 432))

    if cv2.waitKey(1) == 27:
        break

    cv2.imshow('frame', frame)
    time.sleep(0.03)

movie.release()
