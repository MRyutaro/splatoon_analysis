import cv2
import time

# 認識範囲
# 味方ブキアイコン位置
raw_xmin, raw_xmax = 515, 880
raw_ymin, raw_ymax = 30, 150
xmin, xmax = round(raw_xmin/2.5), round(raw_xmax/2.5)
ymin, ymax = round(raw_ymin/2.5), round(raw_ymax/2.5)
# xmin, xmax = 350, 450
# ymin, ymax = 220, 330

# 動画読み込みの設定
movie = cv2.VideoCapture('./data/a.mp4')
# movie = cv2.VideoCapture(0)

# 背景差分の設定
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = movie.read()
    if not ret:
        break

    detframe = frame[ymin:ymax, xmin:xmax]

    # BGR -> grayscale
    gray = cv2.cvtColor(cv2.bitwise_not(detframe), cv2.COLOR_BGR2GRAY)

    # 閾値処理
    _, binary = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

    #  輪郭抽出
    contours, _ = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = list(filter(lambda x: cv2.contourArea(x) > 1600, contours))

    cv2.drawContours(frame, contours, -1, (0, 0, 255), 1, cv2.LINE_AA)

    # 指定範囲に赤枠
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    time.sleep(0.024)

# 撮影用オブジェクトとウィンドウの解放
movie.release()
