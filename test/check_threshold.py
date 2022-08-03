import cv2
import time

movie = cv2.VideoCapture('data/a.mp4')
# movie = cv2.VideoCapture(1)

while True:
    ret, frame = movie.read()
    if not ret:
        break

    # BGR -> grayscale
    gray = cv2.cvtColor(cv2.bitwise_not(frame), cv2.COLOR_BGR2GRAY)

    # 閾値処理
    _, binary = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

    cv2.imshow('frame', binary)
    cv2.waitKey(1)
    time.sleep(0.024)

# 撮影用オブジェクトとウィンドウの解放
movie.release()
