import cv2
import time

# movie = cv2.VideoCapture(1)
movie = cv2.VideoCapture('./data/video/asari.mp4')

while True:
    ret, frame = movie.read()
    if not ret:
        break

    frame = cv2.resize(frame, (768, 432))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    time.sleep(0.02)

movie.release()
